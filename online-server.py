# サーバー設定用ファイル
import socket
from _thread import *
import sys
import pickle
from player import Player

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

players = [Player(300, 0), Player(500, 0)] #修正箇所

def threaded_client(conn, player):
    # global currentId, pos
    conn.send(pickle.dumps(players[player]))  #player1の位置情報 300, 0を送信
    reply = ""
    while True:
        try: 
            data = pickle.loads(conn.recv(2048)) # ここにバグ有 実行されない
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                
                print("Received: " + data)
                print("Sending: " + reply)

            conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print('=== エラー内容 ===')
            print('type:' + str(type(e)))
            print('args:' + str(e.args))
            print('e自身:' + str(e))
            print("error has occured")
            break

    print("Lost Connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1