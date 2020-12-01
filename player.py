import pygame
from pygame.locals import *  #pygame.定数の記述の省略
import random
import Const as C

class Player:

    def __init__(self):
        self.x = 400          #車の横方向の座標を管理するリスト
        self.y = 0            #車のコース上の位置を管理するリスト
        self.lr = 0           #車の左右の向きを管理するリスト
        self.spd = 0          #車の速度を管理するリスト
        self.PLself = 10      #プレイヤーの車の表示位置を定める定数 道路一番手前(画面下)が0
        
        
        
        
    def time_str(self,val):                               # **'**.**という時間の文字列を作る関数
        sec = int(val)                               #引数を整数の秒数にしてsecに代入
        ms  = int((val-sec)*100)                     #秒数の小数点以下の値をmsに代入
        mi  = int(sec/60)                            #分をmiに代入
        return "{}'{:02}.{:02}".format(mi,sec%60,ms)   # **'**.**という文字列を返す
    
    def drive_car(self,game, key, curve, laptime, rec, recbk, tmr,laps,idx): #プレイヤーの車の操作、制御する関数 #修正箇所(returnで値の変更を反映)
        if key[K_LEFT] == 1:  #左キーが押されたら
            if self.lr > -3: #向きが-3より大きければ
                self.lr -= 1  #向きを-1する
            self.x += (self.lr-3)*self.spd/100 - 5      #車の横方向の座標を計算
        elif key[K_RIGHT] == 1:                                        #そうでなく右キーが押されたら
            if self.lr < 3:  #向きが3より小さければ
                self.lr += 1  #向きを+1する
            self.x +=(self.lr+3)*self.spd/100 + 5      #車の横方向の座標を計算
        else:                 #そうでないなら
            self.lr = int(self.lr*0.9)                              #正面向きに近づける
        
        if key[K_a] == 1: #アクセル                                     #Aキーが押されたら
            self.spd += 10    #速度を増やす
        elif key[K_z] == 1:  #ブレーキ                                  #そうでなくzキーが押されたら
            self.spd -= 10   #速度を減らす
        else:                 #そうでないなら
            self.spd -= 0.25 #ゆっくり減速

        if self.spd < 0:  #最低速度                                  #速度が0未満なら
            self.spd = 0    #速度を0にする
        if self.spd > C.CAR_SPD_MAX:  #最高速度                                #最高速度を超えたら
            self.spd = C.CAR_SPD_MAX  #最高速度にする

        self.x -= self.spd * curve[int(self.y + self.PLself) % C.CMAX] / 50 #車の速度と道の曲がりから横方向の座標を計算
        if self.x < 0 + 50:     #左の路肩に接触したら
            self.x = 0 + 50      #横方向の座標を0にして
            self.spd *= 0.9 #減速する
        if self.x > 800 - 50:   #右の路肩に接触したら
            self.x = 800 - 50   #横方向の座標を800にして
            self.spd *= 0.9 #減速する

        self.y += self.spd/100                          #車の速度からコース上の位置を計算
        if self.y > C.CMAX-1:                                         #コース終点を超えたら
            self.y -= C.CMAX  #コースを頭に戻す
            #laptime[laps] = self.time_str(rec-recbk)                            #ラップタイムを計算し代入
            laptime[laps] = self.time_str(game.elapsed_time)                            #ラップタイムを計算し代入  
            recbk = rec           #現在のタイムを保持
            laps += 1             #周回数の値を1増やす
            if laps == C.LAPS:      #周回数がLAPSの値になったら
                idx = 3               #idxを3にしてゴール処理へ
                tmr = 0               #tmrを0にする

        return  laptime, rec, recbk, tmr, laps, idx
            

    def move_player(self, tmr, laps):                                #プレイヤーの車を勝手に動かすための関数
        if self.spd < 200:                                    #速度が100より小さいなら
            self.spd += 3                                         #速度を増やす
            if  tmr % 120 == 1:                                        #一定時間ごとに
                self.lr += random.choice([-1,0,1])                    #向きをランダムに変える
                if self.lr < -3:                                      #向きが-3未満なら-3にする
                    self.lr = -3                                      
                if self.lr > 3:                                       #向きが3を超えたら3にする
                    self.lr = 3
        self.x = self.x + self.lr*self.spd/100          #車の向きと速度から横方向の座標を計算
        if self.x < 50:                                       #左の路肩に近づいたら
            self.x = 50   #それ以上行かないようにして
            self.lr = int(self.lr*0.9)                           #正面向きに近づける
        if self.x > 750:                                      #右の路肩に近づいたら
            self.x = 750  #それ以上行かないようにして
            self.lr = int(self.lr*0.9)                           #正面向きに近づける
        self.y += self.spd/100                              #車の速度からコース上の位置を計算
        if self.y > C.CMAX-1:                                   #コース終点を超えたら
            self.y -= C.CMAX                                         #コースの頭に戻す
            laps += 1             #周回数の値を1増やす
            if laps == C.LAPS:      #周回数がLAPSの値になったら
                laps = 0                #lapsを0にする
        return tmr, laps
        
