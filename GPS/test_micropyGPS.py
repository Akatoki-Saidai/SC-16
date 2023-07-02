from machine import UART
import micropyGPS
from machine import Pin
import utime, gc, _thread
from math import radians, sin, cos
gps_s = UART(0, tx=Pin(0), rx=Pin(1), baudrate=9600, timeout=200)
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
GPSwatch()






