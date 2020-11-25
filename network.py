#Networkクラスのファイル
# network-game-tutorial-5と完全一致
import socket
import pickle
import Const as C

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = C.SERVER 
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode() #プレイヤーが接続したときに最初にplayer1or2が送られる
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))  #pickle形式で送信
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)