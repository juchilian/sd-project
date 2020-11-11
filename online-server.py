# サーバー設定用ファイル
import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '192.168.0.11' # メモだから気にしないで => 'ipconfig' in Terminal => write value of ipv4 
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2) #2人プレイを待つ
print("Waiting for a connection")

currentId = "0"
pos = ["0:300,0", "1:500,0"] #修正箇所
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + reply)
                arr = reply.split(":") # reply中身 (id: x,y)
                id = int(arr[0])
                pos[id] = reply

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = pos[nid][:] # reply = 相手のpos情報
                print("Sending: " + reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))