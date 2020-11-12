"""This is a test program."""
import pygame
import sys
import random
import numpy as np
from math import pi,sin,cos,atan,fabs,sqrt
import time

pygame.init()

#福井はやっぱり死んでほしい 
#イベント毎に処理を分けるための変数
index = 0

#定数定義_色
BLACK  = (  0,  0,  0)
SILBER = (192,192,192)
RED    = (255,  0,  0)
WHITE  = (255,255,255)
GOLD   = (255,216,  0)

#定数定義_マップを作る
MAP_W = 25
MAP_H = 15
MAP_MASS = 50
SIZE = (MAP_W * MAP_MASS,MAP_H * MAP_MASS) #ウインドウサイズ

#画像取込み
img_Wall = pygame.image.load("img/wall2.png")
img_Floor = pygame.image.load("img/concrete.png")
img_car = pygame.image.load("img/car_3.png")

#変数定義(mapに必要なもの)
map = np.zeros((MAP_H,MAP_W),dtype=np.int) #0で初期化

#変数定義(carに必要なもの)

car_speed = 15           #車のスピード
arg = -90                #現在の角度を保存する変数(度)
ARG_ROTATE = 10        #一回ごとの回転角(度)
CAR_W = img_car.get_width() #車の元画像のサイズを取得
CAR_H = img_car.get_height()
car_x,car_y = 0 ,0 #車の中心を計算(初期値)
car_xb,car_yb = car_x, car_y #直前の車の位置を計算


CAR_RANGE = 80 #車の描画範囲(四角形で指定するための一辺の長さ)

img_rotate = pygame.transform.rotozoom(img_car,arg,1)   #回転した画像を代入する変数
car_rotate_w = img_rotate.get_width()  #回転した画像のサイズを取得
car_rotate_h = img_rotate.get_height()
img_car_now = img_rotate
#回転したときの中心のズレを直す変数
reposition_x,reposition_y = 0,0

#ゴールに必要なもの
t1 = time.time() #システムが動き出すときの時刻
tg = 0           #ゴールの瞬間の時刻
goaltime = 0     #システム起動からゴールまでの時間
GOAL_NUM =  3 #最初、何周したらゴールになるかの定数
goal_num = GOAL_NUM #あと何周したらゴールになるかの変数
#スタート&ゴールラインの記述
direction = 0 #0なら時計周り、1なら反時計回り
goal_xs , goal_ys = 625,50
goal_xe , goal_ye = 625,150

#音楽の読み込み
#pygame.mixer.music.load("music/GB-Racing-A05-2(Stage3-Loop180).ogg")


    


def init():
    global car_x,car_y,arg,goal_num,img_rotate,img_car_now,t1
    car_x,car_y = 550 + CAR_W/2 ,60 + CAR_H/2 #車の中心を計算(初期値)
    arg = -90
    goal_num = GOAL_NUM
    img_rotate = pygame.transform.rotozoom(img_car,arg,1)   #回転した画像を代入する変数
    img_car_now = img_rotate
    t1 = time.time()

def music_load():
    if index == 1:
        pygame.mixer.music.load("music/Countdown06-2.mp3")
    if index == 2:
        pygame.mixer.music.load("music/GB-Racing-A05-2(Stage3-Loop180).ogg")
    if index == 3:
        pygame.mixer.music.load("music/GB-Action-D10-1(Clear).ogg")

        
def bgm_play(bg):
    global index
    if index == 0:
        if pygame.mixer.music.get_busy() == True:
             pygame.mixer.music.stop()
    if index == 1:
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play(-1)

    if index == 2:
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.play(-1)
        
    if index == 3:
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play(0)
        index = 4
        music_load()
    
def start_display(bg):
    font_s1 = pygame.font.Font(None,60)
    font_s2 = pygame.font.Font(None,30)
    pygame.draw.rect(bg,GOLD,[500,300,250,150],10)
    pygame.draw.rect(bg,BLACK,[500,300,250,150])
    txt_s1 = font_s1.render("START",True,WHITE)
    txt_s2 = font_s2.render("Push SPACE... ",True,WHITE)
    txt_s3 = font_s2.render("Let's start !!",True,WHITE)
    bg.blit(txt_s1,[550,315])
    bg.blit(txt_s2,[550,365])
    bg.blit(txt_s3,[550,395])
    
def countdown(bg):
    global index
    font_c1 = pygame.font.Font(None,100)
    tc2 = time.time()
    tc3 = 4 - (tc2 - t1)
    if tc3 > 1 and tc3 <= 4: 
        txt_c1 = font_c1.render(str(int(tc3)),True,BLACK)
        bg.blit(txt_c1,[625,325])
    
    if tc3 >= 0 and tc3 <= 1:
        txt_c1 = font_c1.render("START!!",True,BLACK)
        bg.blit(txt_c1,[625,325])
    
    if tc3 <= -0.2:
        index = 2
        music_load()
        init()
        
    

def timer(bg):
    font_t = pygame.font.Font(None,20)
    t2 = time.time()
    elapsed_time = int(t2 - t1)
    pygame.draw.rect(bg,WHITE,[0,0,50,50])
    txt_elapsedtime = font_t.render(str(elapsed_time),True,BLACK)
    bg.blit(txt_elapsedtime,[20,20])
    return elapsed_time

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
    #ゴールラインの記述
    pygame.draw.line(bg,BLACK,[goal_xs,goal_ys],[goal_xe,goal_ye],3)
    
def move_car():
    global car_x,car_y,reposition_x,reposition_y,img_car_now
    global car_rotate_w,car_rotate_h,arg
    global car_xb,car_yb
    key = pygame.key.get_pressed()
    
    arg_rad = arg * pi / 180 #argをラジアンの単位に変換
    
    car_xb = car_x 
    car_yb = car_y
    #print(car_xb)

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
    #print(arg)
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

def goal_judge(bg):
    global goal_num,index,tg,goaltime
    font_gn = pygame.font.Font(None,40)
    txt_gn = font_gn.render(str(goal_num)+" more laps",True,BLACK)
    if goal_num <= GOAL_NUM - 1:
        bg.blit(txt_gn,[100,10])
    
    #ゴール判定
    if direction == 0:
        if car_x >= goal_xs - CAR_H/2 and car_x <= goal_xs - CAR_H/4 and car_y >= goal_ys - 10 and car_y <= goal_ye + 10 :
            print(goal_num) 
            if arg < 0:
                if car_xb <= goal_xs - CAR_H/2:  #左から通り過ぎた場合
                    goal_num = goal_num - 1
                if car_xb >= goal_xs - CAR_H/3:  #右から通り過ぎた場合
                    goal_num = goal_num + 1
                    
            if arg >= 0:
                if car_xb <= goal_xs - CAR_H/2:  #左から通り過ぎた場合
                    goal_num = goal_num - 1
                if car_xb >= goal_xs - CAR_H/3:  #右から通り過ぎた場合
                    goal_num = goal_num + 1
            print(goal_num)
            print(" ")
    if direction == 1:
        if car_x <= goal_xs + CAR_H/2 and car_x >= goal_xs + CAR_H/3 and car_y >= goal_ys and car_y <= goal_ye :
            #print(goal_num) 
            if arg < 0:
                if car_xb >= goal_xs + CAR_H/2:
                    goal_num = goal_num - 1
                if car_xb <= goal_xs + CAR_H/3:
                    goal_num = goal_num + 1
            if arg >= 0:
                if car_xb >= goal_xs + CAR_H/2:
                    goal_num = goal_num - 1
                if car_xb <= goal_xs + CAR_H/3:
                    goal_num = goal_num + 1
    #goal_numが0になったらゴールの表示を行う
    
    if goal_num == 0:
        index = 3
        tg = time.time()
        goaltime = tg - t1
        music_load()

def goal_display(bg):
    font_g = pygame.font.Font(None,60)
    font_gt = pygame.font.Font(None,30)
    pygame.draw.rect(bg,GOLD,[500,300,250,150],10)
    pygame.draw.rect(bg,BLACK,[500,300,250,150])
    txt_goal = font_g.render("GOAL!!",True,WHITE)
    txt_goaltime = font_gt.render("Time:"+str(int(goaltime))+" [s]",True,WHITE)
    txt_next = font_gt.render("Push Escape...",True,WHITE)
    bg.blit(txt_goal,[550,315])
    bg.blit(txt_goaltime,[550,365])
    bg.blit(txt_next,[550,395])

def main():
    global index
    pygame.init()
    pygame.display.set_caption("コースに車を表示する")
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    init()
    music_load()
    make_map()
    

 
    while True:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:   #ウインドウの×ボタンが押されたら
                pygame.quit()               #ゲームを終わる
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #ESCAPEキーが押されたら
                    index = 0 #スタート画面に戻る
                    music_load()
                    init()
                if event.key == pygame.K_F1:      #F1キーが押されたら
                    screen = pygame.display.set_mode(SIZE,pygame.FULLSCREEN)    #フルスクリーンモードにする
                if event.key == pygame.K_F2:      #F2キーが押されたら
                    screen = pygame.display.set_mode(SIZE)   #元のサイズに戻す
                if event.key == pygame.K_SPACE and index == 0:
                    index = 1
                    music_load()
                    init()
        bgm_play(screen)
        if index == 0: #スタート画面
            draw_map(screen)
            move_car()
            draw_car(screen)
            start_display(screen)

        if index == 1: #カウントダウン
            draw_map(screen)
            draw_car(screen)
            countdown(screen)

        
        if index == 2: #ゲームモードの時
            draw_map(screen)
            move_car()
            goal_judge(screen)
            draw_car(screen)
            timer(screen)
            """
            if timer(screen) >= 0 and timer(screen) <= 1:
                font_st = pygame.font.Font(None,100)
                txt_st = font_st.render("START",True,BLACK)
                screen.blit(txt_st,[550,325])
            """
            
                
        #index = 3 の時はゴールの音を流す

        if index == 4: #ゴール後の処理
            draw_map(screen)
            draw_car(screen)
            goal_display(screen)


        
        pygame.display.update()
        clock.tick(20)


    
if __name__ == '__main__':
    main()

