# サーバー設定用ファイル
import socket
from _thread import *
import sys
import pickle
import Const as C
from player import Player
from multigame import MultiGame

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '' # メモだから気にしないで => 'ipconfig' in Terminal => write value of ipv4 
port = 5555

server_ip = socket.gethostbyname(server)
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2) #2人プレイを待つ
print("Waiting for a connection, Server Started")

connected = set() # store ip adrress of connected client
games = {}
idCount = 0

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))  #接続されたらplayer 0 or 1 を送信
    

    reply = ""
    while True:
        try:
            """
                send "reset" or "get" or "move"
                reset-time => ゲームの開始時刻を記録
                get => get Game info from server
                move => 
            """
            data = pickle.loads(conn.recv(4096))

            if gameId in games:
                game = games[gameId] 
                if not data:
                    break
                else:
                    if data == "reset-time":
                        game.start_game()
                    if type(data) == Player: # Player Objectが送られたら
                        game.play(p, data)
                        print(game.bothPos)
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1: #clientが奇数の時
        games[gameId] = MultiGame(gameId)
        print("Creating a new game...")
    else: # clientが偶数の時
        games[gameId].ready = True
        print("Game is ready!!")
        p = 1 # player = 1


    start_new_thread(threaded_client, (conn, p, gameId))