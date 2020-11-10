import pygame
import sys
from math import sin,radians
from pygame.locals import *     #pygame.定数の記述の省略

class Constants:
    #色の定義
    WHITE  = (255,255,255)
    BLACK  = (  0,  0,  0)
    RED    = (255,  0,  0)
    YELLOW = (255,224,  0)
    



class Course:
    #コースの定義
    #道路のカーブを作る基になるデータ
    DATA_LR = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 2, 3, 2, 1, 0, 2, 4,
        2, 4, 2, 0, 0, 0,-2,-2,-4,-4,
        -2,-1, 0, 0, 0, 0, 0, 0, 0
    ]
    #道路の起伏を作る基になるデータ
    DATA_UD = [
        0, 0, 1, 2, 3, 2, 1, 0,-2,-4,
        -2, 0, 0, 0, 0, 0,-1,-2,-3,-4,
        -3,-2,-1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0,-3, 3, 0,-6, 6, 0
    ]
    CLEN = len(DATA_LR)  #左右のデータの要素数を代入した定数
    
    def __init__(self, data_lr, data_ud):
        self.data_lr = data_lr
        self.data_ud = data_ud

class Player:

    def __init__(self):



class Game:

    def __init__(self, game_mode):
        self.game_mode = game_mode # game_mode 1:1人プレイ, 2人プレイ

    def game_start():
        pygame.init() #pygameモジュールの初期化                                                
        pygame.display.set_caption("Pygame Racer") #ウインドウに表示するタイトルを指定
        screen = pygame.display.set_mode((800,600)) #描画面を初期化
        clock = pygame.time.Clock()
        self.load_image()
        self.define_constants()
    

    def load_image(): #画像の読み込み
        img_bg = pygame.image.load("image_pr/bg.png").convert()            #背景(空と地面の絵)
        img_sea = pygame.image.load("image_pr/sea.png").convert_alpha()    #海
        img_obj = [
            None,                                                          #オブジェクト名との整合性をとるためにNoneを入れる
            pygame.image.load("image_pr/board.png").convert_alpha(),       #看板(実際には表示していない)
            pygame.image.load("image_pr/yashi.png").convert_alpha(),       #ヤシの木
            pygame.image.load("image_pr/yacht.png").convert_alpha()        #ヨット
        ]
        img_car = [
            pygame.image.load("image_pr/car00.png").convert_alpha(),       #車(左3)
            pygame.image.load("image_pr/car01.png").convert_alpha(),       #車(左2)
            pygame.image.load("image_pr/car02.png").convert_alpha(),       #車(左1)
            pygame.image.load("image_pr/car03.png").convert_alpha(),       #車(正面)
            pygame.image.load("image_pr/car04.png").convert_alpha(),       #車(右1)
            pygame.image.load("image_pr/car05.png").convert_alpha(),       #車(右2)
            pygame.image.load("image_pr/car06.png").convert_alpha(),       #車(右3)
        ]



def main():
    g = Game(1)
    g.start()


    #道路の板の基本形状を計算
    BOARD_W = [0]*BOARD                            #板の幅を代入するリスト
    BOARD_H = [0]*BOARD                            #板の高さを代入する
    BOARD_UP = [0]*BOARD                           #板の起伏用の値を代入するりすと
    for i in range(BOARD):                         #繰り返しで
        BOARD_W[i] = 10 + (BOARD-i)*(BOARD-i)/12    #幅を計算
        BOARD_H[i] = 3.4*(BOARD-i)/BOARD            #高さを計算
        BOARD_UP[i] = 2*sin(radians(i*1.5))         #起伏の値を三角関数で計算
    
    make_course()                                  #コースデータを作る

    
    vertical = 0                                   #背景の横方向の位置を管理する変数

    while True:                                    #無限ループで処理を続ける
        for event in pygame.event.get():            #pygameのイベントを繰り返しで処理する
            if event.type == QUIT:                   #ウインドウの×ボタンをクリックしたら
                pygame.quit()                        #pygameモジュールの初期化を解除
                sys.exit()                           #プログラムを終了する
        
        
        #描画用の道路のX座標と路面の高低を計算
        di = 0                                                    #道が曲がる向きを計算する変数
        ud = 0                                                    #道の起伏を計算する変数
        board_x = [0]*BOARD                                       #板のx座標を計算するためのリスト
        board_ud = [0]*BOARD                                      #板の工程を計算するためのリスト
        for i in range(BOARD):
            di += curve[int(car_y[0]+i) % CMAX]                      #カーブデータからの道の曲がりを計算
            ud += updown[int(car_y[0]+i) % CMAX]                     #起伏データから起伏を計算
            board_x[i] = 400 - BOARD_W[i]*car_x[0]/800 + di/2        #板のx座標を計算し代入
            board_ud[i] = ud/30                                      #板の高低を計算し代入

        horizon = 400 + int(ud/3)                                 #地平線のy座標を計算しhorizonに代入
        sy = horizon                                              #道路を描き始めるy座標をsyに代入

        vertical = vertical - int(car_spd[0]*di/8000)             #背景の垂直位置を計算
        #背景の垂直位置
        if vertical < 0:                                           #それが0未満になったら
            vertical += 800                                          #800を足す
        if vertical >= 800:                                        #800以上になったら
            vertical -= 800                                          #800を引く

        #フィードの描画
        screen.fill((0,56,255)) #上空の色                           #指定の色で画面を塗りつぶす
        screen.blit(img_bg,[vertical-800,horizon-400])             #空と地面の画像を描画(左側)
        screen.blit(img_bg,[vertical,horizon-400])                 #空と地面の画像を描画(右側)
        screen.blit(img_sea,[board_x[BOARD-1]-780,sy])             #左手奥の海を描画

        #描画用データを基に道路を描く
        for i in range(BOARD-1,0,-1):                              #繰り返しで道路の板を描いていく
            ux = board_x[i]                                        #台形の上底のx座標をuxに代入
            uy = sy - BOARD_UP[i]*board_ud[i]                      #上底のy座標をuyに代入
            uw = BOARD_W[i]                                        #上底の幅をuwに代入
            sy = sy + BOARD_H[i]*(600-horizon)/200                 #台形を描くy座標を次の値にする
            bx = board_x[i-1]                                      #台形の下底のx座標をbxに代入
            by = sy - BOARD_UP[i-1]*board_ud[i-1]                  #下底のy座標をbyに代入
            bw = BOARD_W[i-1]                                      #下底の幅をbwに代入
            col = (160,160,160)                                    #colに板の色を代入
            
            pygame.draw.polygon(screen,col,[[ux,uy],[ux+uw,uy],[bx+bw,by],[bx,by]])   #道路の板を描く

            if int(car_y[0]+i)%10 <= 4:  #左右の黄色線を描画
                pygame.draw.polygon(screen,YELLOW,[[ux,uy],[ux+uw*0.02,uy],[bx+bw*0.02,by],[bx,by]])      #左
                pygame.draw.polygon(screen,YELLOW,[[ux+uw*0.98,uy],[ux+uw,uy],[bx+bw,by],[bx+bw*0.98,by]])   #右

            if int(car_y[0]+i)%20 <= 10:   #白線を描画
                pygame.draw.polygon(screen,WHITE,[[ux+uw*0.24,uy],[ux+uw*0.26,uy],[bx+bw*0.26,by],[bx+bw*0.24,by]])  #左
                pygame.draw.polygon(screen,WHITE,[[ux+uw*0.49,uy],[ux+uw*0.51,uy],[bx+bw*0.51,by],[bx+bw*0.49,by]])  #中央
                pygame.draw.polygon(screen,WHITE,[[ux+uw*0.74,uy],[ux+uw*0.76,uy],[bx+bw*0.76,by],[bx+bw*0.74,by]])  #右


            scale = 1.5*BOARD_W[i]/BOARD_W[0]    #道路横の物体のスケールを計算
            obj_l = object_left[int(car_y[0]+i)%CMAX]   #道路左の物体
            if obj_l == 2: #ヤシの木
                draw_obj(screen,img_obj[obj_l],ux-uw*0.05,uy,scale)
            if obj_l == 3: #ヨット
                draw_obj(screen,img_obj[obj_l],ux-uw*0.5,uy,scale)
            if obj_l == 9: #海
                screen.blit(img_sea,[ux-uw*0.5-780,uy])

            obj_r = object_right[int(car_y[0]+i)%CMAX]  #道路右の物体
            """  #看板はいらないため描画しない
            if obj_r == 1:  #看板
                draw_obj(screen,img_obj[obj_r],ux+uw*1.3,uy,scale)
            """
                
            if i == PLCAR_Y: #PLAYERカー                                                                           #プレイヤーの車の位置なら
                draw_shadow(screen, ux+car_x[0]*BOARD_W[i]/800,uy,200*BOARD_W[i]/BOARD_W[0])                       #車の影を描き
                draw_obj(screen,img_car[3+car_lr[0]],ux+car_x[0]*BOARD_W[i]/800,uy, 0.05+BOARD_W[i]/BOARD_W[0])    #プレイヤーの車を描く
        
        key = pygame.key.get_pressed()                       #keyに全てのキーの状態代入
        drive_car(key)                                       #プレイヤーの車を操作する関数を実行


        pygame.display.update()                      #画面を更新する
        clock.tick(60)                               #フレームレートを指定

if __name__ == '__main__':

    main()