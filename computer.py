import pygame
from pygame.locals import *  #pygame.定数の記述の省略
import random
import Const as C

class Computer:

    def __init__(self):
        self.x = [0]*C.CAR_NUM
        self.y = [0]*C.CAR_NUM
        self.lr = [0]*C.CAR_NUM
        self.spd = [0]*C.CAR_NUM
        for i in range(1,C.CAR_NUM):                              #繰り返しでCOMカーの
            self.x[i] = random.randint(50,750)                #横方向の座標をランダムに決める
            self.y[i] = random.randint(200,C.CMAX-200)          #コース上の位置をランダムに決める
            self.lr[i] = 0                                    #左右の向きを0に(正面向きにする)
            self.spd[i] = random.randint(100,200)             #速度をランダムに決める
    
    def move_car(self,cs):  #COMカーの制御                                #コンピュータの車を制御する関数
        for i in range(cs,C.CAR_NUM):                                     #繰り返しで全ての車を処理する
            if self.spd[i] < 100:                                    #速度が100より小さいなら
                self.spd[i] += 3                                         #速度を増やす
            if i == C.tmr % 120:                                        #一定時間ごとに
                self.lr[i] += random.choice([-1,0,1])                    #向きをランダムに変える
                if self.lr[i] < -3:                                      #向きが-3未満なら-3にする
                    self.lr[i] = -3                                      
                if self.lr[i] > 3:                                       #向きが3を超えたら3にする
                    self.lr[i] = 3
            self.x[i] = self.x[i] + self.lr[i]*self.spd[i]/100          #車の向きと速度から横方向の座標を計算
            if self.x[i] < 50:                                       #左の路肩に近づいたら
                self.x[i] = 50                                            #それ以上行かないようにして
                self.lr[i] = int(self.lr[i]*0.9)                           #正面向きに近づける
            if self.x[i] > 750:                                      #右の路肩に近づいたら
                self.x[i] = 750                                           #それ以上行かないようにして
                self.lr[i] = int(self.lr[i]*0.9)                           #正面向きに近づける
            self.y[i] += self.spd[i]/100                              #車の速度からコース上の位置を計算
            if self.y[i] > C.CMAX-1:                                   #コース終点を超えたら
                self.y[i] -= C.CMAX                                         #コースの頭に戻す

