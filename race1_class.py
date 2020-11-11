import pygame
import sys
from math import sin,radians
from pygame.locals import *  #pygame.定数の記述の省略
### 自作ファイルのインポート ###
import Const as C
from player import Player
from network import Network


class Game:
    def __init__(self):
        # self.game_mode = game_mode # game_mode 1:1人プレイ, 2人プレイ
        self.net = Network()  # Online機能のロード
        self.p1 = self.net.getP()


    def run(self):
        pygame.init() #pygameモジュールの初期化                                                
        pygame.display.set_caption("Pygame Racer") #ウインドウに表示するタイトルを指定
        screen = pygame.display.set_mode((800,600)) #描画面を初期化
        clock = pygame.time.Clock()
        self.load_image() # 画像取り込み
        vertical = 0  #背景の横方向の位置を管理する変数
        curve = [0] * C.CMAX #道が曲がる向きを入れるリスト
        updown = [0] * C.CMAX #道の起伏を入れるリスト
        object_left = [0]*C.CMAX #道路左にある物体の番号を入れるリスト
        object_right = [0] * C.CMAX #道路右にある物体の番号を入れるリスト
        self.make_course(curve, updown, object_left, object_right) #コース設計 

        while True:
            for event in pygame.event.get(): #pygameのイベントを繰り返しで処理する
                if event.type == QUIT: #ウインドウの×ボタンをクリックしたら
                    pygame.quit() #pygameモジュールの初期化を解除
                    sys.exit() #プログラムを終了する
            
            
            
            #描画用の道路のX座標と路面の高低を計算
            di = 0 #道が曲がる向きを計算する変数
            ud = 0 #道の起伏を計算する変数
            board_x = [0] * C.BOARD #板のx座標を計算するためのリスト
            board_ud = [0] * C.BOARD #板の工程を計算するためのリスト
            for i in range(C.BOARD):
                di += curve[int(self.p1.y + i) % C.CMAX] #カーブデータからの道の曲がりを計算
                ud += updown[int(self.p1.y + i) % C.CMAX] #起伏データから起伏を計算
                board_x[i] = 400 - C.BOARD_W[i] * self.p1.x / 800 + di / 2 #板のx座標を計算し代入
                board_ud[i] = ud / 30 #板の高低を計算し代入

            horizon = 400 + int(ud / 3) #地平線のy座標を計算しhorizonに代入
            sy = horizon #道路を描き始めるy座標をsyに代入

            vertical = vertical - int(self.p1.spd * di / 8000) #背景の垂直位置を計算
            #背景の垂直位置
            if vertical < 0: #それが0未満になったら
                vertical += 800 #800を足す
            if vertical >= 800: #800以上になったら
                vertical -= 800 #800を引く

            #フィードの描画
            screen.fill((0, 56, 255)) #上空の色 #指定の色で画面を塗りつぶす
            screen.blit(self.img_bg, [vertical - 800, horizon - 400]) #空と地面の画像を描画(左側)
            screen.blit(self.img_bg, [vertical, horizon - 400]) #空と地面の画像を描画(右側)
            screen.blit(self.img_sea, [board_x[C.BOARD - 1] - 780, sy]) #左手奥の海を描画

            #描画用データを基に道路を描く
            for i in range(C.BOARD - 1, 0, -1): #繰り返しで道路の板を描いていく
                ux = board_x[i] #台形の上底のx座標をuxに代入
                uy = sy - C.BOARD_UP[i] * board_ud[i] #上底のy座標をuyに代入
                uw = C.BOARD_W[i] #上底の幅をuwに代入
                sy = sy + C.BOARD_H[i] * (600 - horizon) / 200 #台形を描くy座標を次の値にする
                bx = board_x[i-1] #台形の下底のx座標をbxに代入
                by = sy - C.BOARD_UP[i - 1] * board_ud[i - 1] #下底のy座標をbyに代入
                bw = C.BOARD_W[i - 1] #下底の幅をbwに代入
                col = (160, 160, 160) #colに板の色を代入
                
                pygame.draw.polygon(screen, col, [[ux, uy], [ux + uw, uy], [bx + bw, by], [bx, by]]) #道路の板を描く

                if int(self.p1.y+i)%10 <= 4:  #左右の黄色線を描画
                    pygame.draw.polygon(screen, C.YELLOW, [[ux, uy], [ux + uw * 0.02, uy], [bx + bw * 0.02, by], [bx, by]]) #左
                    pygame.draw.polygon(screen, C.YELLOW, [[ux + uw * 0.98, uy], [ux + uw, uy], [bx + bw, by], [bx + bw * 0.98, by]]) #右

                if int(self.p1.y+i)%20 <= 10:   #白線を描画
                    pygame.draw.polygon(screen, C.WHITE, [[ux + uw * 0.24, uy], [ux + uw * 0.26, uy], [bx + bw * 0.26, by], [bx + bw * 0.24, by]]) #左
                    pygame.draw.polygon(screen, C.WHITE, [[ux + uw * 0.49, uy], [ux + uw * 0.51, uy], [bx + bw * 0.51, by], [bx + bw * 0.49, by]]) #中央
                    pygame.draw.polygon(screen, C.WHITE, [[ux + uw * 0.74, uy], [ux + uw * 0.76, uy], [bx + bw * 0.76, by], [bx + bw * 0.74, by]]) #右


                scale = 1.5 * C.BOARD_W[i] / C.BOARD_W[0] #道路横の物体のスケールを計算
                obj_l = object_left[int(self.p1.y + i) % C.CMAX] #道路左の物体
                if obj_l == 2: #ヤシの木
                    self.draw_obj(screen, self.img_obj[obj_l], ux - uw * 0.05, uy, scale)
                if obj_l == 3: #ヨット
                    self.draw_obj(screen, self.img_obj[obj_l], ux - uw * 0.5, uy, scale)
                if obj_l == 9: #海
                    screen.blit(self.img_sea, [ux - uw * 0.5-780, uy])

                obj_r = object_right[int(self.p1.y + i) % C.CMAX] #道路右の物体
                """  #看板はいらないため描画しない
                if obj_r == 1:  #看板
                    self.draw_obj(screen,img_obj[obj_r],ux+uw*1.3,uy,scale)
                """
                    
                if i == self.p1.PLself: #PLAYERカーがプレイヤーの車の位置なら
                    self.draw_shadow(screen, ux + self.p1.x * C.BOARD_W[i] / 800, uy, 200 * C.BOARD_W[i] / C.BOARD_W[0]) #車の影を描く
                    self.draw_obj(screen, self.img_car[3 + self.p1.lr], ux + self.p1.x * C.BOARD_W[i] / 800, uy, 0.05+ C.BOARD_W[i] / C.BOARD_W[0]) #プレイヤーの車を描く
            
            key = pygame.key.get_pressed() #keyに全てのキーの状態代入
            self.p1.drive_car(key, curve) #プレイヤーの車を操作する関数を実行 
            
            #オンライン通信
            p2 = self.net.send(self.p1)
            
            pygame.display.update() #画面を更新する
            clock.tick(60)  #フレームレートを指定


    def make_course(self, curve, updown, object_left, object_right): #コースデータを作る関数
        for i in range(C.CLEN):  
            lr1 = C.DATA_LR[i] #カーブデータをlr1に代入   
            lr2 = C.DATA_LR[(i+1)%C.CLEN] #次のカーブデータをlr2に代入
            ud1 = C.DATA_UD[i] #起伏のデータをud1に代入
            ud2 = C.DATA_UD[(i+1)%C.CLEN] #次の起伏のデータをud2に代入
            for j in range(C.BOARD):
                pos = j + C.BOARD * i #リストの添え字を計算しposに代入
                curve[pos] = lr1 * (C.BOARD - j) / C.BOARD + lr2 * j / C.BOARD #道が曲がる向きを計算し代入
                updown[pos] = ud1 * (C.BOARD - j) / C.BOARD + ud2 * j / C.BOARD #道の起伏を計算し代入
                
                if j == 60:
                    object_right[pos] = 1 #看板
                if i%8 < 7:
                    if j%12 == 0 :
                        object_left[pos] = 2 #ヤシの木
                else:
                    if j%20 == 0:
                        object_left[pos] = 3 #ヨット
                if j%12 == 6:
                    object_left[pos] = 9  #海
        
        # return curve, updown, object_left, object_right 


    def load_image(self): #画像の読み込み
        self.img_bg = pygame.image.load("image_pr/bg.png").convert()            #背景(空と地面の絵)
        self.img_sea = pygame.image.load("image_pr/sea.png").convert_alpha()    #海
        self.img_obj = [
            None, #オブジェクト名との整合性をとるためにNoneを入れる
            pygame.image.load("image_pr/board.png").convert_alpha(), #看板(実際には表示していない)
            pygame.image.load("image_pr/yashi.png").convert_alpha(), #ヤシの木
            pygame.image.load("image_pr/yacht.png").convert_alpha()  #ヨット
        ]
        self.img_car = [
            pygame.image.load("image_pr/car00.png").convert_alpha(),       #車(左3)
            pygame.image.load("image_pr/car01.png").convert_alpha(),       #車(左2)
            pygame.image.load("image_pr/car02.png").convert_alpha(),       #車(左1)
            pygame.image.load("image_pr/car03.png").convert_alpha(),       #車(正面)
            pygame.image.load("image_pr/car04.png").convert_alpha(),       #車(右1)
            pygame.image.load("image_pr/car05.png").convert_alpha(),       #車(右2)
            pygame.image.load("image_pr/car06.png").convert_alpha(),       #車(右3)
        ]

    @staticmethod
    def draw_obj(bg, img, x, y, sc): #座標とスケールを受け取り、物体を描く関数
        img_rz = pygame.transform.rotozoom(img, 0, sc)      #拡大縮小した画像を受け取る
        w = img_rz.get_width()                              #その画像の幅をwに代入
        h = img_rz.get_height()                             #その画像の高さをhに代入
        bg.blit(img_rz, [x - w / 2, y - h])                 #画像を描く

    @staticmethod
    def draw_shadow(bg, x, y, siz): #車の影を表示する関数
        shadow = pygame.Surface([siz, siz / 4]) #描画面(サーフェース)を用意する
        shadow.fill(C.RED) #その描画面を赤で埋めつくす
        shadow.set_colorkey(C.RED)                            #Surfaceの透過色を指定
        shadow.set_alpha(128)                               #Surfaceの透明度を指定
        pygame.draw.ellipse(shadow, C.BLACK, [0, 0, siz, siz / 4]) #描画面に黒で楕円を描く
        bg.blit(shadow, [x - siz / 2, y - siz / 4]) #楕円を描いた描画面をゲーム画面に転送



if __name__ == '__main__':
    g = Game()
    g.run()