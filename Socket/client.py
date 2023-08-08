import socket
import time
host = "192.168.11.60"#アドレス
port = 80#ポート

def client(host,port,msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ソケットオブジェクトの作成

    client.connect((host, port)) #サーバーに接続します

    message = str(msg)
    print('Send : %s' % message)
    client.send(message.encode()) #データを送信します
    response = client.recv(4096) #一度に受け取るデータのサイズ。レシーブは適当な2の累乗に(大きすぎるとダメ）
    print('Received: %s' % response.decode())#送られてきたデータをデコード

if __name__ == "__main__":
    while True:
        msg = 12334
        client(host,port,msg)
        time.sleep(1)