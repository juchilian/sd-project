import pygame
from pygame.locals import *  #pygame.定数の記述の省略
import Const as C


class Player:

    def __init__(self, startx, starty):
        self.x = startx            #車の横方向の座標を管理するリスト
        self.y = starty            #車のコース上の位置を管理するリスト
        self.lr = 0           #車の左右の向きを管理するリスト
        self.spd = 0          #車の速度を管理するリスト
        self.PLself = 10  #プレイヤーの車の表示位置を定める定数 道路一番手前(画面下)が0
        
    def drive_car(self, key, curve): #プレイヤーの車の操作、制御する関数
        if key[K_LEFT] == 1: #左キーが押されたら
            if self.lr > -3: #向きが-3より大きければ
                self.lr -= 1 #向きを-1する
            self.x += (self.lr - 3) * self.spd / 100 - 5 #車の横方向の座標を計算
        elif key[K_RIGHT] == 1: #そうでなく右キーが押されたら
            if self.lr < 3: #向きが3より小さければ
                self.lr += 1 #向きを+1する
            self.x += (self.lr + 3) * self.spd / 100 + 5 #車の横方向の座標を計算
        else:
            self.lr = int(self.lr*0.9) #正面向きに近づける
        
        if key[K_a] == 1: #アクセル                                     #Aキーが押されたら
            self.spd += 3                                            #速度を増やす
        elif key[K_z] == 1:  #ブレーキ                                  #そうでなくzキーが押されたら
            self.spd -= 10                                            #速度を減らす
        else:                                                          #そうでないなら
            self.spd -= 0.25                                          #ゆっくり減速

        if self.spd < 0:  #最低速度                                  #速度が0未満なら
            self.spd = 0                                             #速度を0にする
        if self.spd > 200:  #最高速度 #最高速度を超えたら
            self.spd = 200 #最高速度にする

        self.x -= self.spd * curve[int(self.y + self.PLself) % C.CMAX] / 50 #車の速度と道の曲がりから横方向の座標を計算
        if self.x < 0: #左の路肩に接触したら
            self.x = 0 #横方向の座標を0にして
            self.spd *= 0.9 #減速する
        if self.x > 800: #右の路肩に接触したら
            self.x = 800 #横方向の座標を800にして
            self.spd *= 0.9 #減速する

        self.y += self.spd / 100 #車の速度からコース上の位置を計算
        if self.y > C.CMAX - 1: #コース終点を超えたら
            self.y -= C.CMAX #コースを頭に戻す
