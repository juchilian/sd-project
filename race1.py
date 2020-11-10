import pygame
import sys
from math import sin,radians
from pygame.locals import *     #pygame.定数の記述の省略

#色の定義
WHITE  = (255,255,255)
BLACK  = (  0,  0,  0)
RED    = (255,  0,  0)
YELLOW = (255,224,  0)

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
CLEN = len(DATA_LR)       #左右のデータの要素数を代入した定数



BOARD = 120                #道路を描く板の枚数を定める定数
CMAX = BOARD*CLEN          #コースの長さ(要素数)を定める定数
curve = [0]*CMAX           #道が曲がる向きを入れるリスト
updown = [0]*CMAX          #道の起伏を入れるリスト
object_left = [0]*CMAX     #道路左にある物体の番号を入れるリスト
object_right = [0]*CMAX    #道路右にある物体の番号を入れるリスト

CAR = 30                   #車の数を定める定数
car_x = [0]*CAR            #車の横方向の座標を管理するリスト
car_y = [0]*CAR            #車のコース上の位置を管理するリスト
car_lr = [0]*CAR           #車の左右の向きを管理するリスト
car_spd = [0]*CAR          #車の速度を管理するリスト
PLCAR_Y = 10               #プレイヤーの車の表示位置を定める定数 道路一番手前(画面下)が0

def make_course():         #コースデータを作る関数
    for i in range(CLEN):  
        lr1 = DATA_LR[i]                    #カーブデータをlr1に代入   
        lr2 = DATA_LR[(i+1)%CLEN]           #次のカーブデータをlr2に代入
        ud1 = DATA_UD[i]                    #起伏のデータをud1に代入
        ud2 = DATA_UD[(i+1)%CLEN]           #次の起伏のデータをud2に代入
        for j in range(BOARD):
            pos = j + BOARD*i                                      #リストの添え字を計算しposに代入
            curve[pos]  = lr1*(BOARD-j)/BOARD + lr2*j/BOARD        #道が曲がる向きを計算し代入
            updown[pos] = ud1*(BOARD-j)/BOARD + ud2*j/BOARD        #道の起伏を計算し代入
            
            if j == 60:
                object_right[pos] = 1 #看板
            if i%8 < 7:
                if j%12 == 0 :
                    object_left[pos] = 2 #ヤシの木
            else:
                if j%20 == 0:
                    object_left[pos] = 3 #ヨット
            if j%12 == 6:
                object_left[pos] = 9 #海

def draw_obj(bg, img, x, y, sc):                        #座標とスケールを受け取り、物体を描く関数
    img_rz = pygame.transform.rotozoom(img,0,sc)        #拡大縮小した画像を受け取る
    w = img_rz.get_width()                              #その画像の幅をwに代入
    h = img_rz.get_height()                             #その画像の高さをhに代入
    bg.blit(img_rz,[x-w/2,y-h])                         #画像を描く

def draw_shadow(bg,x,y,siz):                            #車の影を表示する関数
    shadow = pygame.Surface([siz,siz/4])                #描画面(サーフェース)を用意する
    shadow.fill(RED)                                    #その描画面を赤で埋めつくす
    shadow.set_colorkey(RED)                            #Surfaceの透過色を指定
    shadow.set_alpha(128)                               #Surfaceの透明度を指定
    pygame.draw.ellipse(shadow,BLACK,[0,0,siz,siz/4])   #描画面に黒で楕円を描く
    bg.blit(shadow,[x-siz/2,y-siz/4])                   #楕円を描いた描画面をゲーム画面に転送

def drive_car(key):                                                #プレイヤーの車の操作、制御する関数
    if key[K_LEFT] == 1:                                           #左キーが押されたら
        if car_lr[0] > -3:                                          #向きが-3より大きければ
            car_lr[0] -= 1                                           #向きを-1する
        car_x[0] = car_x[0] + (car_lr[0]-3)*car_spd[0]/100 - 5      #車の横方向の座標を計算
    elif key[K_RIGHT] == 1:                                        #そうでなく右キーが押されたら
        if car_lr[0] < 3:                                           #向きが3より小さければ
            car_lr[0] += 1                                           #向きを+1する
        car_x[0] = car_x[0] + (car_lr[0]+3)*car_spd[0]/100 + 5      #車の横方向の座標を計算
    else:                                                          #そうでないなら
        car_lr[0] = int(car_lr[0]*0.9)                              #正面向きに近づける
    
    if key[K_a] == 1: #アクセル                                     #Aキーが押されたら
        car_spd[0] += 3                                             #速度を増やす
    elif key[K_z] == 1:  #ブレーキ                                  #そうでなくzキーが押されたら
        car_spd[0] -= 10                                            #速度を減らす
    else:                                                          #そうでないなら
        car_spd[0] -= 0.25                                          #ゆっくり減速

    if car_spd[0] < 0:  #最低速度                                  #速度が0未満なら
        car_spd[0] = 0                                             #速度を0にする
    if car_spd[0] > 200:  #最高速度                                #最高速度を超えたら
        car_spd[0] = 200                                           #最高速度にする

    car_x[0] -= car_spd[0]*curve[int(car_y[0]+PLCAR_Y)%CMAX]/50   #車の速度と道の曲がりから横方向の座標を計算
    if car_x[0] < 0:                                              #左の路肩に接触したら
        car_x[0] = 0                                               #横方向の座標を0にして
        car_spd[0] *= 0.9                                          #減速する
    if car_x[0] > 800:                                            #右の路肩に接触したら
        car_x[0] = 800                                             #横方向の座標を800にして
        car_spd[0] *= 0.9                                          #減速する

    car_y[0] = car_y[0] + car_spd[0]/100                          #車の速度からコース上の位置を計算
    if car_y[0] > CMAX-1:                                         #コース終点を超えたら
        car_y[0] -= CMAX                                           #コースを頭に戻す

    #print(car_x[0])
    #print(car_y[0])


def main():
    pygame.init()                                                      #pygameモジュールの初期化
    pygame.display.set_caption("Pygame Racer")                         #ウインドウに表示するタイトルを指定
    screen = pygame.display.set_mode((800,600))                        #描画面を初期化
    clock = pygame.time.Clock()                                        #clockオブジェクトを作成

    #画像の読み込み
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

    #道路の板の基本形状を計算
    BOARD_W = [0]*BOARD                            #板の幅を代入するリスト
    BOARD_H = [0]*BOARD                            #板の高さを代入する
    BOARD_UP = [0]*BOARD                           #
    for i in range(BOARD):
        BOARD_W[i] = 10 + (BOARD-i)*(BOARD-i)/12
        BOARD_H[i] = 3.4*(BOARD-i)/BOARD
        BOARD_UP[i] = 2*sin(radians(i*1.5))
    
    make_course()

    
    vertical = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        
        #描画用の道路のX座標と路面の高低を計算
        di = 0
        ud = 0
        board_x = [0]*BOARD
        board_ud = [0]*BOARD
        for i in range(BOARD):
            di += curve[int(car_y[0]+i) % CMAX]
            ud += updown[int(car_y[0]+i) % CMAX]
            board_x[i] = 400 - BOARD_W[i]*car_x[0]/800 + di/2
            #board_x[i] = 400 - BOARD_W[i]/2 + di/2
            board_ud[i] = ud/30

        horizon = 400 + int(ud/3)
        sy = horizon

        vertical = vertical - int(car_spd[0]*di/8000)
        #背景の垂直位置
        if vertical < 0:
            vertical += 800
        if vertical >= 800:
            vertical -= 800

        #フィードの描画
        screen.fill((0,56,255)) #上空の色
        screen.blit(img_bg,[vertical-800,horizon-400])
        screen.blit(img_bg,[vertical,horizon-400])
        screen.blit(img_sea,[board_x[BOARD-1]-780,sy]) #一番奥の海

        #描画用データを基に道路を描く
        for i in range(BOARD-1,0,-1):
            ux = board_x[i]
            uy = sy - BOARD_UP[i]*board_ud[i]
            uw = BOARD_W[i]
            sy = sy + BOARD_H[i]*(600-horizon)/200
            bx = board_x[i-1]
            by = sy - BOARD_UP[i-1]*board_ud[i-1]
            bw = BOARD_W[i-1]
            col = (160,160,160)
            
            pygame.draw.polygon(screen,col,[[ux,uy],[ux+uw,uy],[bx+bw,by],[bx,by]])

            if int(car_y[0]+i)%10 <= 4:  #左右の黄色線
                pygame.draw.polygon(screen,YELLOW,[[ux,uy],[ux+uw*0.02,uy],[bx+bw*0.02,by],[bx,by]])
                pygame.draw.polygon(screen,YELLOW,[[ux+uw*0.98,uy],[ux+uw,uy],[bx+bw,by],[bx+bw*0.98,by]])

            if int(car_y[0]+i)%20 <= 10:   #白線
                pygame.draw.polygon(screen,WHITE,[[ux+uw*0.24,uy],[ux+uw*0.26,uy],[bx+bw*0.26,by],[bx+bw*0.24,by]])
                pygame.draw.polygon(screen,WHITE,[[ux+uw*0.49,uy],[ux+uw*0.51,uy],[bx+bw*0.51,by],[bx+bw*0.49,by]])
                pygame.draw.polygon(screen,WHITE,[[ux+uw*0.74,uy],[ux+uw*0.76,uy],[bx+bw*0.76,by],[bx+bw*0.74,by]])


            scale = 1.5*BOARD_W[i]/BOARD_W[0]
            obj_l = object_left[int(car_y[0]+i)%CMAX]   #道路左の物体
            if obj_l == 2: #ヤシの木
                draw_obj(screen,img_obj[obj_l],ux-uw*0.05,uy,scale)
            if obj_l == 3: #ヨット
                draw_obj(screen,img_obj[obj_l],ux-uw*0.5,uy,scale)
            if obj_l == 9: #海
                screen.blit(img_sea,[ux-uw*0.5-780,uy])

            obj_r = object_right[int(car_y[0]+i)%CMAX]  #道路右の物体
            """
            if obj_r == 1:  #看板
                draw_obj(screen,img_obj[obj_r],ux+uw*1.3,uy,scale)
            """
                
            if i == PLCAR_Y: #PLAYERカー
                draw_shadow(screen, ux+car_x[0]*BOARD_W[i]/800,uy,200*BOARD_W[i]/BOARD_W[0])
                draw_obj(screen,img_car[3+car_lr[0]],ux+car_x[0]*BOARD_W[i]/800,uy, 0.05+BOARD_W[i]/BOARD_W[0])
        
        key = pygame.key.get_pressed()
        drive_car(key)


        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
