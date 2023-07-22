import micropyGPS
from machine import Pin,UART
import utime, gc, _thread
from math import *

class GPS():
    def __init__(self,uart_number=0,tx=Pin(12),rx=Pin(13),baudrate=9600,timeout=2000):
        self.gps_s = UART(uart_number, tx=tx, rx=rx, baudrate=baudrate, timeout=timeout)
        micropyGPS.MicropyGPS.supported_sentences.update({'GNGSA': micropyGPS.MicropyGPS.gpgsa})
        self.gps = micropyGPS.MicropyGPS(9, 'dd')
        self.pre_lat = 0
        self.pre_long = 0

    def GPSwatch(self):
        n = 0
        tm_last = 0
        satellites = dict()
        satellites_used = dict()
        utime.sleep_ms(300)
        len = self.gps_s.any()

        if len>0:
            b = self.gps_s.read(len)
            for x in b:
                if 10 <= x <= 126:
                    stat = self.gps.update(chr(x))
                    if stat:
                        tm = self.gps.timestamp
                        tm_now = (tm[0] * 3600) + (tm[1] * 60) + int(tm[2])
                        if (tm_now - tm_last) >= 10:
                            n += 1
                            tm_last = tm_now
                            #print("{} {}:{}:{}".format(self.gps.date_string(), tm[0], tm[1], int(tm[2])))
        
                            data1 = self.gps.latitude[0]
                            data2 = self.gps.longitude[0]
                            #print(f'lat:{self.gps.latitude[0]},long:{self.gps.longitude[0]}')
                            return data1,data2
    def cal_x_y(self,lat,lon):
        gol_lat = 35.862734
        gol_lon = 139.607167
        p = 3600 * 180/3.1415926535897932#今は秒になっている。分のときは、180/math.pi()
        F = 298.257222101
        a = 6378137#[m]
        m0 = 0.9999
        n = 1/(2*F-1)
        t = sinh(atanh(sin(lat))-(2*sqrt(n)/(1+n)*sin(lat)))
        t_bar = sqrt(1+t**2)
        lam_c = cos(lon-gol_lon)
        lam_s = sin(lon-gol_lon)
        guzai = atan(t/lam_c)
        eta = atanh(lam_s/t_bar)
        alpha1 = 0.5*n-(2/3)*n**2 + (5/16)*n**3+(41/180)*n**4-(127/288)*n**5
        alpha2 = (13/48)*n**2-(3/5)*n**3+(557/1440*n**4)+(281/630)*n**5
        alpha3 = (61/240)*n**3-(103/140)*n**4+(15061/26880)*n**5
        alpha4 = (49561/161280)*n**4-(179/168)*n**5
        alpha5 = (34729/80640)*n**5
        A0 = 1+((n**2)/4)+((n**4)/64)
        A1 = (-3/2)*(n-(n**3)/8-(n**5)/64)
        A2 = (15/16)*(n**2-(n**4)/4)
        A3 = (-35/48)*(n**3-(15/16)*n**5)
        A4 = (315/512)*n**4
        A5 = (-693/1280)*n**5
        S0 = ((m0*a)/(1+n))*((A0*gol_lat/p)+A1*sin(2*1*gol_lat)+A2*sin(2*2*gol_lat)+A3*sin(2*3*gol_lat)+A4*sin(2*4*gol_lat)+A5*sin(2*5*gol_lat))
        A_bar =((m0*a)/(1+n))*A0
    
        x = A_bar*(guzai+alpha1*sin(2*1*guzai)*cosh(2*1*eta)+alpha2*sin(2*2*guzai)*cosh(2*2*eta)+alpha3*sin(2*3*guzai)*cosh(2*3*eta)+alpha4*sin(2*4*guzai)*cosh(2*4*eta)+alpha5*sin(2*5*guzai)*cosh(2*5*eta)-S0)
        y = A_bar*(eta+alpha1*cos(2*1*eta)*sinh(2*1*eta)+alpha2*cos(2*2*eta)*sinh(2*2*eta)+alpha3*cos(2*3*eta)*sinh(2*3*eta)+alpha4*cos(2*4*eta)*sinh(2*4*eta)+alpha5*cos(2*5*eta)*sinh(2*5*eta))
        return x,y

    def cal_distance(self,goal_lat,goal_long,lat,long):#単位系は[km]
        pole_radius = 6356752.314245                  # 極半径
        equator_radius = 6378137.0                    # 赤道半径
        # 緯度経度をラジアンに変換
        goal_lat = radians(goal_lat)
        goal_long = radians(goal_long)
        lat = radians(lat)
        long = radians(long)

        lat_difference = goal_lat - lat       # 緯度差
        lon_difference = goal_long - long       # 経度差
        lat_average = (goal_lat + lat) / 2    # 平均緯度

        e2 = (pow(equator_radius, 2) - pow(pole_radius, 2)) / pow(equator_radius, 2)  # 第一離心率^2

        w = sqrt(1- e2 * pow(sin(lat_average), 2))

        m = equator_radius * (1 - e2) / pow(w, 3) # 子午線曲率半径

        n = equator_radius / w                         # 卯酉線曲半径

        distance = sqrt(pow(m * lat_difference, 2) + pow(n * lon_difference * cos(lat_average), 2)) # 距離計測

        #print(distance)#m kmにしたいなら/1000して
        return distance
        
    def cal_azimuth(self,goal_lat, goal_long, lat, long):#出てくる値は国土地理院のと比べると3度くらい多く出た
        # Radian角に修正
        _goal_lat = goal_lat*3.1415926535897932/180
        goal_long = goal_long*3.1415926535897932/180
        lat = lat*3.1415926535897932/180
        long = long*3.1415926535897932/180
        Δx = lat - goal_lat
        _y = sin(Δx)
        _x = cos(goal_long) * tan(long) - sin(goal_long) * cos(Δx)
        psi = atan2(_y, _x) * 180 / 3.1415926535897932
        if psi < 0:
            return 360 + atan2(_y, _x) * 180 / 3.1415926535897932
        else:
            return atan2(_y, _x) * 180 / 3.1415926535897932

if __name__ == '__main__':
    while True:
        try:
            goal_lat = 35.8627962
            goal_long = 139.6071776
            gps = GPS()
            data1,data2 = gps.GPSwatch()
            print(data1,data2)
            print(gps.cal_azimuth(goal_lat,goal_long,data1,data2))
            gps.cal_distance(goal_lat,goal_long,data1,data2)
        except TypeError:
            pass
    """
    while True:
        gps_data = gps.GPSwatch()
        if(gps_data == None):
            continue
        print(gps_data)
        #print(gps.distance(goal_lat,goal_long))
        """