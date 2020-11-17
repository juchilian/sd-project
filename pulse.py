import socket
import matplotlib.pyplot as pyplot

class Pulse:

    def __init__(self):
        #define standby port number as 50000
        self.PORT = 50000
        #assign buffer size as 1024
        self.BUFFER_SIZE = 1024
        self.bpm_list = []
        self.data = 0
        self.pulse_socket()
        self.convert_spd()

    def pulse_socket(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #listen 
            #wait for access
            s.bind(('192.168.11.7', self.PORT))
            s.listen()
            while True:
                (connection, client) = s.accept()
                try:
                    print('Client connected', client)
                    #receive data from server
                    self.data = connection.recv(self.BUFFER_SIZE)

                    #このデータが心拍データ。関数の返り値にできれば藤井のやつと簡単に組み合わせられる！！
                    # connection.send(data)
                    self.bpm_list.append(int(float(data)))
                    print(self.bpm_list)

                finally:
                    connection.close()



