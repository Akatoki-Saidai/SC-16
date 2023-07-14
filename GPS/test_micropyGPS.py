"""
参考文献
https://keisan.casio.jp/exec/system/1257670779
https://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc/algorithm/bl2xy/bl2xy.htm
http://k-ichikawa.blog.enjoy.jp/etc/HP/js/sokuchi/sok2S.html
"""
from machine import UART
import micropyGPS
from machine import Pin
import utime, gc, _thread
from math import *
gps_s = UART(0, tx=Pin(0), rx=Pin(1), baudrate=9600)
micropyGPS.MicropyGPS.supported_sentences.update({'GNGSA': micropyGPS.MicropyGPS.gpgsa})
gps = micropyGPS.MicropyGPS(9, 'dd')
def GPSwatch():
    n = 0
    tm_last = 0
    satellites = dict()
    satellites_used = dict()
    while True:
        utime.sleep_ms(100)
        len = gps_s.any()
        mozi = gps.date_string(formatting='s_mdy', century='20')
        print(mozi)
        str = '%.10f %c, %.10f %c' % (gps.latitude[0], gps.latitude[1], gps.longitude[0], gps.longitude[1])
        print(str)
        if len>0:
            b = gps_s.read(len)
            for x in b:
                if 10 <= x <= 126:
                    stat = gps.update(chr(x))
                    if stat:
                        tm = gps.timestamp
                        tm_now = (tm[0] * 3600) + (tm[1] * 60) + int(tm[2])
                        if (tm_now - tm_last) >= 10:
                            n += 1
                            tm_last = tm_now
                            print("{} {}:{}:{}".format(gps.date_string(), tm[0], tm[1], int(tm[2])))
                            str = '%.10f %c, %.10f %c' % (gps.latitude[0], gps.latitude[1], gps.longitude[0], gps.longitude[1])
                            print(str)
                            if gps.satellite_data_updated():
                                putSatellites(satellites, gps.satellite_data, tm_now)
                            putSatellitesUsed(satellites_used, gps.satellites_used, tm_now)
                            if (n % 10) == 0:
                                print("Mem free:", gc.mem_free())
                                gc.collect()
def putSatellites(sats, new_sats, tm):
    for k, v in new_sats.items():  # 衛星の辞書に新しい衛星データーと現在時刻を追加する
        sats.update({k: (v, tm)})
    for k, v in sats.items():  # 衛星の辞書中で300秒以上古いものを削除する
        if tm - v[1] > 300:
            print('pop(%s)' % str(k))
            sats.pop(k)
def putSatellitesUsed(sats_used, sats, tm):
    for x in sats:
        sats_used.update({x: tm})
    for k, v in sats_used.items():
        if tm - v > 300:
            print('pop_used(%s)' % str(k))
            sats_used.pop(k)
    print(sats_used)
"""
def cal_x_y(lat,lon):
    gol_lat = 0
    gol_lon = 0
    p = 3600 * 180/math.pi()#今は秒になっている。分のときは、180/math.pi()
    F = 298.257222101
    a = 6378137#[m]
    m0 = 0.9999
    n = 1/(2*F-1)
    t = sinh(atanh(sin(lat))-(2*sqrt(n)/(1+n)sin(lat)))
    t_bar = sqrt(1+t**2)
    lam_c = cos(lon-gol_lon)
    lam_s = sin(lon-gol_lon)
    guzai = atan(t/lam_c)
    eta = atanh(lam_s/t_bar)
    alpha1 = 0.5*n-(2/3)*n**2 + (5/16)*n**3+(41/180)*n**4-(127/288)*n**5
    alpha2 = (13/48)*n**2-(3/5)*n**3+(557/1440*n**4)+(281/630)*n**5
    aplha3 = (61/240)*n**3-(103/140)*n**4+(15061/26880)*n**5
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
def cal_degree(lat,lon,gol_lat,gol_lon):
    r = 6378.137[km]
    delta = gol_lon-lon
    d = r*acos(sin(lat)*sin(gol_lat)+cos(lat)*cos(gol_lat)*delta)#距離
    phai = 90-atan2(sin(delta),cos(lat)*tan(gol_lat)-sin(lat)*cos(delta))#角度
    return d,phai
"""
GPSwatch()














