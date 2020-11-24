#PC側で動かすコード
import socket
import matplotlib.pyplot as pyplot

#define standby port number as 50000
PORT = 50000
#assign buffer size as 1024
BUFFER_SIZE = 1024

bpm_list = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #listen 
    #wait for access
    s.bind(('192.168.100.112', PORT))
    s.listen()
    while True:
        (connection, client) = s.accept()
        try:
            print('Client connected', client)
            #receive data from server
            data = connection.recv(BUFFER_SIZE)

            #このデータが心拍データ。関数の返り値にできれば藤井のやつと簡単に組み合わせられる！！
            # connection.send(data)
            # bpm_list.append(int(float(data)))
            print(data)

        finally:
            connection.close()