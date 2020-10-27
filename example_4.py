import pygame
import sys
import random
import numpy as np
from math import pi,sin,cos,atan,fabs,sqrt

#定数定義_初期化
BLACK  = (  0,  0,  0)
SILBER = (192,192,192)

#定数定義_マップを作る
MAP_W = 25
MAP_H = 15
MAP_MASS = 50
SIZE = (MAP_W * MAP_MASS,MAP_H * MAP_MASS) #ウインドウサイズ

#画像取込み
img_Wall = pygame.image.load("wall2.png")
img_Floor = pygame.image.load("concrete.png")
img_car = pygame.image.load("car_3.png")

#変数定義(mapに必要なもの)
map = np.zeros((MAP_H,MAP_W),dtype=np.int) #0で初期化

#変数定義(carに必要なもの)

car_speed = 15           #車のスピード
arg = -90                #現在の角度を保存する変数(度)
ARG_ROTATE = 10        #一回ごとの回転角(度)
CAR_W = img_car.get_width() #車の元画像のサイズを取得
CAR_H = img_car.get_height()
car_x,car_y = 600 + CAR_W/2 ,60 + CAR_H/2 #車の中心を計算(初期値)


CAR_RANGE = 80 #車の描画範囲(四角形で指定するための一辺の長さ)

img_rotate = pygame.transform.rotozoom(img_car,arg,1)   #回転した画像を代入する変数
car_rotate_w = img_rotate.get_width()  #回転した画像のサイズを取得
car_rotate_h = img_rotate.get_height()
img_car_now = img_rotate
#回転したときの中心のズレを直す変数
reposition_x,reposition_y = 0,0

def make_map():
    global map
    #周りの壁を作成
    map[0:MAP_H:MAP_H-1,:] = 1
    map[:,0:MAP_W:MAP_W-1] = 1

    #コース作成
    map[3,3:MAP_W-3:1] = 1
    map[3:12:1,3] = 1
    map[11,3:MAP_W-3:1] = 1
    map[6,6:MAP_W-1:1] = 1
    map[7:9:1,6:MAP_W-3:6] = 1
    map[9:11:1,9:MAP_W-3:6] = 1

def draw_map(bg):
    for y in range(MAP_H):
        for x in range(MAP_W):
            X = x * MAP_MASS
            Y = y * MAP_MASS
            if map[y,x] == 0:
                bg.blit(img_Floor,[X,Y])
            if map[y,x] == 1:
                bg.blit(img_Wall,[X,Y])

def move_car():
    global car_x,car_y,reposition_x,reposition_y,img_car_now
    global car_rotate_w,car_rotate_h,arg
    key = pygame.key.get_pressed()
    
    arg_rad = arg * pi / 180 #argをラジアンの単位に変換
    

    #UPキーが押されたら
    if key[pygame.K_UP] == 1:
        car_x = car_x - car_speed * sin(arg_rad)
        car_y = car_y - car_speed * cos(arg_rad)
    #DOWNキーが押されたら
    if key[pygame.K_DOWN] == 1:
        car_x = car_x + car_speed * sin(arg_rad)
        car_y = car_y + car_speed * cos(arg_rad)
    #RIGHTキーが押されたら
    if key[pygame.K_RIGHT] == 1:
        arg = arg - ARG_ROTATE
        img_rotate = pygame.transform.rotozoom(img_car,arg,1)
        car_rotate_w = img_rotate.get_width()
        car_rotate_h = img_rotate.get_height()
        reposition_x = (car_rotate_w - CAR_W) / 2
        reposition_y = (car_rotate_h - CAR_H) / 2
        img_car_now = img_rotate
    #LEFTキーが押されたら
    if key[pygame.K_LEFT] == 1:
        arg = arg + ARG_ROTATE
        img_rotate = pygame.transform.rotozoom(img_car,arg,1)
        car_rotate_w = img_rotate.get_width()
        car_rotate_h = img_rotate.get_height()
        reposition_x = (car_rotate_w - CAR_W) / 2
        reposition_y = (car_rotate_h - CAR_H) / 2
        img_car_now = img_rotate
    
    

    #角度を真上から測って±90度に設定
    if arg > 180:
        arg = arg - 360
    if arg < -180:
        arg = arg + 360
    #画面からはみ出さないようにする
    #上下左右各々の方向から±90度を設定
    arg_o = fabs(arg)
    arg_o_up = arg_o                 #上方向の角度
    arg_o_right_left = fabs(90-arg_o)#左右方向の角度
    arg_o_down = fabs(180-arg_o)     #下方向の角度
    

    #それぞれをラジアンに直す
    arg_o_up_rad = arg_o_up * pi / 180
    arg_o_right_left_rad = arg_o_right_left * pi / 180
    arg_o_down_rad = arg_o_down * pi / 180
    
    #上下左右の壁と車の中心からの距離を計算
    overhang_up = ( sqrt(CAR_H*CAR_H + CAR_W*CAR_W) / 2 ) * cos( arg_o_up_rad - atan(CAR_W/CAR_H))
    overhang_right_left = ( sqrt(CAR_H*CAR_H + CAR_W*CAR_W) / 2 ) * cos( arg_o_right_left_rad - atan(CAR_W/CAR_H)) 
    overhang_down = ( sqrt(CAR_H*CAR_H + CAR_W*CAR_W) / 2 ) * cos( arg_o_down_rad - atan(CAR_W/CAR_H))
    #進行方向にはみ出しそうになったら位置を修正する
    if car_y  <= 0 + overhang_up : #上
        car_y = 0 + overhang_up 
    if car_y  >= SIZE[1] - overhang_down : #下
        car_y = SIZE[1] - overhang_down 
    if car_x  <= 0 + overhang_right_left : #左
        car_x = 0 + overhang_right_left 
    if car_x   >= SIZE[0] - overhang_right_left : #右
        car_x = SIZE[0] - overhang_right_left
    #後退方向にはみ出しそうになったら位置を修正する
    #左右は上記と同じコードで大丈夫なため省略
    if car_y  <= 0 + overhang_down : #上
        car_y = 0 + overhang_down 
    if car_y  >= SIZE[1] - overhang_up : #下
        car_y = SIZE[1] - overhang_up 

    #壁への衝突判定
    for y in range(MAP_H):
        for x in range(MAP_W):
            if map[y,x] == 1:
                kabe_up = y * MAP_MASS
                kabe_down = y * MAP_MASS + MAP_MASS
                kabe_right = x * MAP_MASS + MAP_MASS
                kabe_left = x * MAP_MASS
                #進行方向にはみ出しそうになったら位置を修正する
                if car_y  <= kabe_down + overhang_up  and car_y >= kabe_up : #上
                    if car_x >= kabe_left and car_x <= kabe_right:
                        car_y = kabe_down + overhang_up 
                if car_y >= kabe_up - overhang_down and car_y <= kabe_down : #下
                    if car_x >= kabe_left and car_x <= kabe_right:
                        car_y = kabe_up - overhang_down 
                if car_x  <= kabe_right + overhang_right_left and car_x >= kabe_left :#左
                    if car_y >= kabe_up and car_y <= kabe_down:
                        car_x = kabe_right + overhang_right_left 

                if car_x  >= kabe_left - overhang_right_left and car_x <= kabe_right :#右
                    if car_y >= kabe_up and car_y <= kabe_down:
                        car_x = kabe_left - overhang_right_left 

                #後退方向にはみ出しそうになったら位置を修正する
                if car_y <= kabe_down + overhang_down and car_y >= kabe_up : #上
                    if car_x >= kabe_left and car_x <= kabe_right:
                        car_y = kabe_down + overhang_down 

                if car_y  >= kabe_up - overhang_up and car_y <= kabe_down : #下
                    if car_x >= kabe_left and car_x <= kabe_right:
                        car_y = kabe_up - overhang_up 
 

def draw_car(bg):
    #描画している車のサイズを取得
    car_now_w = img_car_now.get_width()
    car_now_h = img_car_now.get_height()
    bg.blit(img_car_now,[car_x - CAR_RANGE/2,car_y - CAR_RANGE/2],
                    ((car_now_w/2)- CAR_RANGE/2,(car_now_h/2)- CAR_RANGE/2,
                     CAR_RANGE,CAR_RANGE))

   
    pygame.draw.rect(bg,BLACK,[car_x - CAR_RANGE/2 , car_y-CAR_RANGE/2 ,CAR_RANGE,CAR_RANGE],1)

def main():
    pygame.init()
    pygame.display.set_caption("コースに車を表示する")
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    make_map()
    draw_map(screen)

    while True:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:   #ウインドウの×ボタンが押されたら
                pygame.quit()               #ゲームを終わる
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #ESCAPEキーが押されたら
                    pygame.quit()                #ゲームを終わる
                    sys.exit()
                if event.key == pygame.K_F1:      #F1キーが押されたら
                    screen = pygame.display.set_mode(SIZE,pygame.FULLSCREEN)    #フルスクリーンモードにする
                if event.key == pygame.K_F2:      #F2キーが押されたら
                    screen = pygame.display.set_mode(SIZE)   #元のサイズに戻す
        draw_map(screen)
        draw_car(screen)
        move_car()

        pygame.display.update()
        clock.tick(20)

if __name__ == '__main__':
    main()

