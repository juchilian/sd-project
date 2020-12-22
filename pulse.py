import socket
import time
import random
import numpy as np

class Pulse:
    def __init__(self):
        #define standby port number as 50000
        self.PORT = 50000
        #assign buffer size as 1024
        self.BUFFER_SIZE = 1024
        self.time = 0
        # self.data = self.pulse_socket()    
        #IPアドレスへの接続のためのレッスン状態

    #心拍数を計測してself.dataに格納
    def pulse_socket(self):
        #試したい場合のコード
        # self.data = random.randint(0,200)
        # print(self.data)
        # return self.data


        #心拍が取れている場合のコード    
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # コネクションを試みる
            s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)# ここで毎回切断
            s.bind(('192.168.100.112', self.PORT))
            s.listen()
            (connection, client) = s.accept()

            # try:
            print('Client connected', client)
            #receive data from server
            #データがリアルタイムに変化する
            try:
                self.data = connection.recv(self.BUFFER_SIZE)
            #このデータが心拍データ。関数の返り値にできれば藤井のやつと簡単に組み合わせられる！！
            # connection.send(data)
                return self.data
            
            finally:
                connection.close()



pulse = Pulse()
pulse.pulse_socket()