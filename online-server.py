# サーバー設定用ファイル
import socket
from _thread import *
import sys

server = '192.168.0.13' # メモだから気にしないで => 'ipconfig' in Terminal => write value of ipv4 
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2) #2人プレイを待つ
print("Waiting for a connection")

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

# currentId = "0"
pos = [(300, 0), (500, 0)] #修正箇所

def threaded_client(conn, player):
    # global currentId, pos
    conn.send(str.encode(make_pos(pos[player])))  #player1の位置情報 300, 0を送信
    print("値：", make_pos(pos[player])) # 出力：300,0
    # currentId = "1"
    reply = ""
    while True:
        try: 
            data = read_pos(conn.recv(2048).decode()) # ここにバグ有 実行されない
            print("サーバー data: " + data) 
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                
                print("Received: " + data)
                # 一つ前のコード
                # arr = reply.split(":") # reply中身 (id: x,y)
                # id = int(arr[0])
                # pos[id] = reply

                # if id == 0: nid = 1
                # if id == 1: nid = 0

                # reply = pos[nid][:] # reply = 相手のpos情報
                print("Sending: " + reply)

            conn.sendall(str.encode(make_pos(reply)))
        except Exception as e:
            print('=== エラー内容 ===')
            print('type:' + str(type(e)))
            print('args:' + str(e.args))
            print('message:' + e.message)
            print('e自身:' + str(e))
            print("error has occured")
            break

    print("Lost Closed")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1