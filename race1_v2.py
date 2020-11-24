import pygame
import sys
from math import sin,radians
import random
from pygame.locals import *  #pygame.定数の記述の省略
import Const as C
from player import Player
from computer import Computer
from network import Network
from multigame import MultiGame
from canvas import Canvas
import time


class Game:
    def __init__(self):
        self.p1 = Player(300, 0) # Player1定義
        self.com = Computer()
        self.cvs = Canvas()
        # Parameters(Varaible)
        self.idx = 0
        self.tmr = 0  #タイマーの変数
        self.time = 0  #timeモジュールを使った時間の計測のための変数
        self.laps = 0  #何周目かを管理する変数
        self.rec = 0  #走行時間を測る変数
        self.recbk = 0  #ラップタイム計算用の変数
        self.laptime = ["0'00.00"] * C.LAPS  #ラップタイム表示用のリスト
        self.mycar = 0  #車選択用の変数
        self.mymode = 0  #モード選択用の変数
        
        

    def run(self):
        pygame.init() #pygameモジュールの初期化                                                
        pygame.display.set_caption("Pygame Racer") #ウインドウに表示するタイトルを指定
        screen = pygame.display.set_mode((1100,600)) #描画面を初期化
        clock = pygame.time.Clock()
        fnt_s = pygame.font.Font(None,40)    #小さい文字
        fnt_m = pygame.font.Font(None,50)    #中くらいの文字
        fnt_l = pygame.font.Font(None,120)   #大きい文字
        self.load_image() # 画像取り込み
        self.load_sound() # サウンド取り込み
        vertical = 0  #背景の横方向の位置を管理する変数
        curve = [0] * C.CMAX           #道が曲がる向きを入れるリスト
        updown = [0] * C.CMAX          #道の起伏を入れるリスト
        object_left = [0]*C.CMAX     #道路左にある物体の番号を入れるリスト
        object_right = [0] * C.CMAX  #道路右にある物体の番号を入れるリスト
        self.make_course(curve, updown, object_left, object_right) #コース設計 #修正箇所(returnで値の変更を反映)

        while True:                                    #無限ループで処理を続ける
            for event in pygame.event.get():            #pygameのイベントを繰り返しで処理する
                if event.type == QUIT:                   #ウインドウの×ボタンをクリックしたら
                    pygame.quit()                        #pygameモジュールの初期化を解除
                    sys.exit()                           #プログラムを終了する
            self.tmr += 1
            self.cvs.update_canvas(self, curve, updown, vertical, screen, object_left, object_right, fnt_s, fnt_m, fnt_l)
            key = pygame.key.get_pressed()                       #keyに全てのキーの状態代入
            self.manage_game(key, curve, screen, fnt_s, fnt_m, fnt_l)
            pygame.display.update()                      #画面を更新する
            clock.tick(60)                               #フレームレートを指定

    def manage_game(self, key, curve, screen, fnt_s, fnt_m, fnt_l):
        '''
            indexの説明
            0 => タイトル画面
            1 => カウントダウン時
            2 => レース中
            3 => ゴール時
            4 => 車種選択の時
            5 => モード選択の時
        '''
        if self.idx == 0:                                                     #idxが0(タイトル画面)のとき
            screen.blit(self.img_title,[120,120])                               #タイトルロゴを表示
            
            self.cvs.draw_text(screen,"[S] Select your car",400,320,C.WHITE,fnt_m)       #[S] Select your car の文字を表示
            self.cvs.draw_text(screen,"[M] Select mode",400,400,C.WHITE,fnt_m)
            self.tmr, self.laps = self.p1.move_player(self.tmr, self.laps) #プレイヤーの車をただ動かすだけ
            self.com.move_car(1, self.tmr)                                                #コンピュータの車を動かす
            
            if key[K_s] != 0:                                               #Sキーが押されたら         
                self.idx = 4                                                         #idxを4にして車種選択に移行
            if key[K_m] != 0:                                               #Mキーが押されたら
                self.idx = 5                                                    #idxを5にしてモード選択に移行

        if self.idx == 1: #idxが1(カウントダウン)のとき
            time_c = time.time()
            time_cd = 3 - int(time_c - self.time)
            self.music_play()
            self.cvs.draw_text(screen,str(time_cd),400,240,C.YELLOW,fnt_l)
            if time_cd <= 0 :
                self.idx = 2  #idxを2にしてレースへ                
                self.tmr = 0                                                              #tmrを0にする
                self.time = time.time()                                                             #このときの時刻を計算
            if self.mymode == 1:  #multiplaymodeなら
                #オンライン通信にて敵位置取得＆自分位置送信
                self.game = self.n.send(self.p1)

        if self.idx == 2:                                                    #idxが2(レース中)のとき
            if self.tmr < 60:                                                      #60フレームの間だけ
                self.cvs.draw_text(screen,"Go!",400,240,C.RED,fnt_l)                     #GO!と表示 
            
            self.music_play()
            self.rec = self.rec + 1/60                                                 #走行時間をカウント
            self.laptime, self.rec, self.recbk, self.tmr, self.laps, self.idx = self.p1.drive_car(key, curve, self.laptime, self.rec, self.recbk, self.tmr,self.laps,self.idx) #プレイヤーの車を動かせるように
            self.com.move_car(1, self.tmr)          #コンピュータの車を動かす
            self.collision_judge(1)  #衝突判定
            if self.mymode == 1:  #multiplaymodeなら
                #オンライン通信にて敵位置取得＆自分位置送信
                self.game = self.n.send(self.p1)


        if self.idx == 3:              #idxが3(ゴール)のとき
            self.music_play()
            self.cvs.draw_text(screen,"GOAL!",400,240,C.GREEN,fnt_l)                #GOAL!と表示       
            self.p1.spd = self.p1.spd * 0.96 #プレイヤーの車の速度を落とす
            self.p1.y = self.p1.y + self.p1.spd/100 #コース上を進ませる
            self.com.move_car(1,self.tmr)                    #コンピュータの車を動かす
            if self.tmr > 60*8:                        #8秒経過したら
                self.laps = 0
                self.idx = 0                                 #idxを0にしてタイトルに戻る

        if self.idx == 4:                                                      #idxが4(車種選択)のとき
            self.tmr, self.laps = self.p1.move_player(self.tmr, self.laps)               #プレイヤーの車を動かす                                   #プレイヤーの車をただ動かすだけ
            self.com.move_car(1,self.tmr)                                                #コンピュータの車を動かす
            self.car_select(screen,fnt_m,key)
            

        if self.idx == 5:                                                      #idxが5(モード選択)のとき
            self.tmr, self.laps = self.p1.move_player(self.tmr, self.laps)               #プレイヤーの車を動かす                                   #プレイヤーの車をただ動かすだけ
            self.com.move_car(1,self.tmr)                                                #コンピュータの車を動かす
            self.mode_select(screen,fnt_m,key)
            

    def collision_judge(self,cs):
        if self.idx == 2:
            for i in range(cs,C.CAR_NUM):
                cx = self.com.x[i] - self.p1.x  #プレイヤーの車との横方向の距離
                
                cy = self.com.y[i]-(self.p1.y+self.p1.PLself) % C.CMAX                         #プレイヤーの車とのコース上の距離
                if -100 <= cx and cx <= 100 and -10 <= cy and cy <= 10:       #それらがこの範囲内なら
                    #衝突時の座標変化、速度の入れ替えと減速
                    self.p1.x -= cx/4                                          #プレイヤーの車を横に移動
                    self.com.x[i] += cx/4                                          #コンピュータの車を横に移動
                    self.p1.spd, self.com.spd[i] = self.com.spd[i]*0.3, self.p1.spd*0.3   #2つの車の速度を入れ替え、減速する
                    self.se_crash.play()                                           #衝突音を出力する


    def make_course(self, curve, updown, object_left, object_right): #コースデータを作る関数 #修正箇所(returnで値の変更を反映)
        for i in range(C.CLEN):
            lr1 = C.DATA_LR[i]                    #カーブデータをlr1に代入   
            lr2 = C.DATA_LR[(i+1)%C.CLEN]           #次のカーブデータをlr2に代入
            ud1 = C.DATA_UD[i]                    #起伏のデータをud1に代入
            ud2 = C.DATA_UD[(i+1)%C.CLEN]           #次の起伏のデータをud2に代入
            for j in range(C.BOARD):
                pos = j + C.BOARD*i                                      #リストの添え字を計算しposに代入
                curve[pos]  = lr1*(C.BOARD-j)/C.BOARD + lr2*j/C.BOARD        #道が曲がる向きを計算し代入
                updown[pos] = ud1*(C.BOARD-j)/C.BOARD + ud2*j/C.BOARD        #道の起伏を計算し代入
                
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


    def car_select(self,bg,fnt_m,key):
        self.cvs.draw_text(bg,"Select your car",400,160,C.WHITE,fnt_m)      #Select your car を表示
        for i in range(3):                                                  #繰り返しで
            x = 160+240*i                                                       #xに選択用の枠のx座標を代入
            y = 300                                                             #yに選択用の枠のy座標を代入
            col = C.BLACK                                                       #colにBLACkを代入
            if i == self.mycar:                                                    #選択している車種なら
                col = (0,128,255)                                                   #colに明るい青の値を代入
            pygame.draw.rect(bg,col,[x-100,y-80,200,160])                   #colの色で枠を描く
            self.cvs.draw_text(bg,"["+str(i+1)+"]",x,y-50,C.WHITE,fnt_m)        #[n]の文字を表示
            bg.blit(self.img_car[3+i*7],[x-100,y-20])                       #それぞれの車を描画
        self.cvs.draw_text(bg,"[Enter] OK!",400,440,C.GREEN,fnt_m)          #[Enter] OK! を表示
        if key[K_1] == 1:                                                   #1キーが押されたら
            self.mycar = 0                                                         #mycarに0を代入(赤い車)
        if key[K_2] == 1:                                                   #2キーが押されたら
            self.mycar = 1                                                         #mycarに1を代入(青い車)
        if key[K_3] == 1:                                                   #3キーが押されたら
            self.mycar = 2                                                         #mycarに2を代入(黄色の車)
        if key[K_RETURN] == 1:                                              #Enterキーが押されたら
            self.idx = 0                                                           #idxを0にしてタイトル画面に戻る


    def mode_select(self,bg,fnt_m,key):
        self.cvs.draw_text(bg,"Select mode",400,160,C.WHITE,fnt_m)          #Select mode を表示
        for i in range(2):                                                  #繰り返しで
            x = 200+400*i                                                       #xに選択用の枠のx座標を代入
            y = 300                                                             #yに選択用の枠のy座標を代入
            col = C.BLACK                                                       #colにBLACkを代入
            if i == self.mymode:                                                    #選択している車種なら
                col = (0,128,255)                                                   #colに明るい青の値を代入
            pygame.draw.rect(bg,col,[x-120,y-120,240,240])                   #colの色で枠を描く
            self.cvs.draw_text(bg,"["+str(i+1)+"]",x,y-90,C.WHITE,fnt_m)        #[n]の文字を表示
            if i == 0:
                self.cvs.draw_text(bg,"Single play",x,y-40,C.WHITE,fnt_m)
            if i == 1:
                self.cvs.draw_text(bg,"Multi play",x,y-40,C.WHITE,fnt_m)
            
            bg.blit(self.img_mode[i],[x-100,y-10])                       #それぞれの車を描画

        self.cvs.draw_text(bg,"[Enter] Start game",400,460,C.GREEN,fnt_m)          #[Enter] OK! を表示
        self.cvs.draw_text(bg,"[B] Back to title",400,540,C.WHITE,fnt_m)          #[Enter] OK! を表示
        if key[K_1] == 1:
            self.mymode = 0  #mymodeに0を代入(single play)
        if key[K_2] == 1: #2キーが押されたら
            self.mymode = 1 #mymodeに1を代入(multi play)
        
        if key[K_RETURN] != 0: 
            if self.mymode == 0: #singleモードが選択されたら
                self.p1.__init__(300, 0)  #プレイヤーの車を初期化
                self.com.__init__()  #コンピュータの車を初期化
                self.idx = 1  #idxを1にしてカウントダウンに
                self.time = time.time()  #このときの時刻を記録
                self.tmr = 0  #タイマーを0に
                self.laps = 0  #周回数を0に
                self.rec = 0  #走行時間を0に
                self.recbk = 0  #ラップタイム計算用の変数を0に
                for i in range(self.laps):  #繰り返しで
                    self.laptime[i] = "0'00.00"  #ラップタイムを0'00.00に
            if self.mymode == 1:  #multiモードが選択されたら
                run = True
                self.n = Network()
                player = int(self.n.getP()) # プレイヤーNumをGet
                print("You are player", player)
                if player == 0:
                    self.p1 = Player(300, 0)
                elif player == 1:
                    self.p1 = Player(500, 0)

                while run:
                    try:
                        self.game = self.n.send(self.p1)  # Game object全てが戻ってくる
                    except:
                        run = False
                        print("Couldn't get game")
                        break
                    if not (self.game.connected()):  # 1台のみ接続中
                        print("waiting for opponent")
                    else:  # 両者が繋がったら
                        print("Game Id is", self.game.id)
                        self.idx = 1  # カウントダウンフェーズに移行
                        break

        if key[K_b] != 0:
            self.idx = 0   #タイトル画面に戻る


    def load_image(self): #画像の読み込み
        self.img_title = pygame.image.load("image_pr/title_sd.png").convert_alpha()    #タイトルロゴ
        self.img_bg = pygame.image.load("image_pr/bg.png").convert()            #背景(空と地面の絵)
        self.img_sea = pygame.image.load("image_pr/sea.png").convert_alpha()    #海
        self.img_obj = [
            None,                                                          #オブジェクト名との整合性をとるためにNoneを入れる
            pygame.image.load("image_pr/board.png").convert_alpha(),       #看板(実際には表示していない)
            pygame.image.load("image_pr/yashi.png").convert_alpha(),       #ヤシの木
            pygame.image.load("image_pr/yacht.png").convert_alpha()        #ヨット
        ]
        self.img_car = [
            pygame.image.load("image_pr/car00.png").convert_alpha(),       #車(左3)_赤
            pygame.image.load("image_pr/car01.png").convert_alpha(),       #車(左2)
            pygame.image.load("image_pr/car02.png").convert_alpha(),       #車(左1)
            pygame.image.load("image_pr/car03.png").convert_alpha(),       #車(正面)
            pygame.image.load("image_pr/car04.png").convert_alpha(),       #車(右1)
            pygame.image.load("image_pr/car05.png").convert_alpha(),       #車(右2)
            pygame.image.load("image_pr/car06.png").convert_alpha(),       #車(右3)
            pygame.image.load("image_pr/car10.png").convert_alpha(),       #車(左3)_青
            pygame.image.load("image_pr/car11.png").convert_alpha(),       #車(左2)
            pygame.image.load("image_pr/car12.png").convert_alpha(),       #車(左1)
            pygame.image.load("image_pr/car13.png").convert_alpha(),       #車(正面)
            pygame.image.load("image_pr/car14.png").convert_alpha(),       #車(右1)
            pygame.image.load("image_pr/car15.png").convert_alpha(),       #車(右2)
            pygame.image.load("image_pr/car16.png").convert_alpha(),       #車(右3)
            pygame.image.load("image_pr/car20.png").convert_alpha(),       #車(左3)_黄色
            pygame.image.load("image_pr/car21.png").convert_alpha(),       #車(左2)
            pygame.image.load("image_pr/car22.png").convert_alpha(),       #車(左1)
            pygame.image.load("image_pr/car23.png").convert_alpha(),       #車(正面)
            pygame.image.load("image_pr/car24.png").convert_alpha(),       #車(右1)
            pygame.image.load("image_pr/car25.png").convert_alpha(),       #車(右2)
            pygame.image.load("image_pr/car26.png").convert_alpha()        #車(右3)
        ]
        
        self.img_mode = [
            pygame.image.load("image_pr/singlemode.png").convert_alpha(),
            pygame.image.load("image_pr/multimode.png").convert_alpha()
        ]
        
    
    def music_play(self):
        if self.idx == 0:   #タイトル画面
            pass
        if self.idx == 1:   #カウントダウン画面
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.load("sound_pr/countdown.mp3")                          #BGMを読み込み
                pygame.mixer.music.set_volume(1.0)                                   #音を小さくして
                pygame.mixer.music.play(0)     
        if self.idx == 2:   #レース中
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.load("sound_pr/bgm.ogg")                          #BGMを読み込み
                pygame.mixer.music.set_volume(0.2)                                   #音を小さくして
                pygame.mixer.music.play(-1)     
        if self.idx == 3:   #ゴール画面
            if self.tmr == 1:                                                      #tmrが1なら
                pygame.mixer.music.stop()                                             #bgmを停止
            if self.tmr == 30:                                                     #tmrが30になったら
                pygame.mixer.music.load("sound_pr/goal.ogg")                          #BGMを読み込み
                pygame.mixer.music.set_volume(0.2)                                   #音を小さくして
                pygame.mixer.music.play(0)     
        if self.idx == 4:   #車種選択画面
            pass
        if self.idx == 5:   #モード選択画面
            pass   


    def load_sound(self):
        self.se_crash = pygame.mixer.Sound("sound_pr/crash.ogg")   #SE(衝突音)の読み込み
        self.se_crash.set_volume(0.2)                              #衝突音が大きすぎたので小さくする




if __name__ == '__main__':
    g = Game()
    g.run()