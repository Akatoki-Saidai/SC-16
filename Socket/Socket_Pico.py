import network
import socket
from time import sleep
import machine
import time 
#参考文献：https://tech-and-investment.com/raspberrypi-picow-5-webserver/
# Wi-Fi ルーターのSSIDとパスワードです。
# お使いの設定に書き換えてください。
class Socket_rev():
    def __init__(self):
        self.ssid = 'Buffalo-G-2CE8'
        self.password = 'ea8548fsfe4av'

    #
    # Wi-Fiに接続する関数です
    #
    def connect(self):
        #Connect to WLAN
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.password)
        while wlan.isconnected() == False:
            print('Waiting for connection...')
            sleep(1)
        ip = wlan.ifconfig()[0]
        print(f'Connected on {ip}')
        return ip

    #
    # クライアント(ブラウザ)からの接続に対応する関数です
    #
    def serve(self,connection):
        #Start a web server
        self.client = connection.accept()[0]
        request = self.client.recv(1024)
        request = str(request)
        try:
            request = request.split()[ 1]
        except IndexError:
            pass
        self.client.close()
        return (request)

    
    #
    # データをやり取りする口(ソケット)を
    # 作成する関数です
    #    
    def open_socket(self,ip):
        # Open a socket
        address = (ip, 80)
        connection = socket.socket()
        connection.bind(address)
        connection.listen(1)
        return connection

    def main(self):
        #
        # メインの処理部分です
        #
        t1 = time.time()
        try:
            # Wi-Fiに接続し、IPアドレスを取得します
            ip = self.connect()

            # IPアドレスを使って、データをやり取りするソケットを作ります
            connection = self.open_socket(ip)

            # ソケットを使って、クライアント(ブラウザ)からの接続を待ちます
            # (内部で無限ループ)
            while True:
                msg = (self.serve(connection))
                print(type(msg))
                #msg = msg.split()
                print(msg)
                

        #
        # プログラムが中断された場合は、この処理に飛び、 
        # デバイスをリセットします
        #
        except KeyboardInterrupt:
            machine.reset()
if __name__ == '__main__':
    k = Socket_rev()           
    k.main()