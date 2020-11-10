import pygame
import sys
from math import sin,radians
from pygame.locals import *  #pygame.定数の記述の省略

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
PLCAR_Y = 10  #プレイヤーの車の表示位置を定める定数 道路一番手前(画面下)が0


class Player:

    def __init__(self, init_x, car_img):
        self.car_x = init_x
        self.car_y = 0
        self.car_spd = 0
        self.car_img = car_img

    def 

