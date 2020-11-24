import socket

#心拍が取れている場合のコード  
# 以下のコード全体をwhile分内部に入れてはいけない！  
def connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #listen 
            #wait for access
            #接続しているwifi次第で変える！
        s.bind(('192.168.11.7', 50000))
        s.listen()

        while True:
    #コネクションを試みる
        # 接続を受け付けます。ソケットはアドレスにbind済みで、listen中である必要があります。
        # 戻り値は (conn, address) のペアで、 connは接続を通じてデータの送受信を行うための
        # 新しい ソケットオブジェクト、 address は接続先でソケットにbindしているアドレスを示します。
            (connection, client) = s.accept()

            # try:
            print('Client connected', client)
            #receive data from server
            #データがリアルタイムに変化する
            try:
                data = connection.recv(1024)
            #このデータが心拍データ。関数の返り値にできれば藤井のやつと簡単に組み合わせられる！！
            # connection.send(data)
            # print(self.data)
                print(data)
                # return data
            
            finally:
                connection.close()

    

while True:
    connection()