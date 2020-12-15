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
from KCF_python import Kcf_python

class Game:
    def __init__(self):
        pygame.init() #pygameモジュールの初期化                                                
        self.p1 = Player(300, 0) # Player1定義
        self.com = Computer()
        self.cvs = Canvas()
        # self.kcf = Kcf_python()
        # Parameters(Varaible)
        self.idx = 8
        self.tmr = 0                           #タイマーの変数
        self.time = 0                          #timeモジュールを使った時間の計測のための変数
        self.laps = 0                          #何周目かを管理する変数
        self.rec = 0                           #走行時間を測る変数
        self.recbk = 0                         #ラップタイム計算用の変数
        self.laptime = ["0'00.00"] * C.LAPS #ラップタイム表示用のリスト
        self.mycar = 0                         #車選択用の変数
        self.mymode = 0                        #モード選択用の変数
        self.mylocation = 0                    #場所選択用の変数
        self.mybgm = 0
        self.elapsed_time = 0
        self.elapsed_time_lap = 0
        self.kcf = Kcf_python()
        # self.value = 0
        
    #ファイル実行
    def run(self):
        pygame.display.set_caption("Pygame Racer")  #ウインドウに表示するタイトルを指定
        clock = pygame.time.Clock()
        self.load_image() # 画像取り込み
        self.load_bgm()   #bgm取り込み
        self.load_sound() # サウンド取り込み
        
        while True:                              #無限ループで処理を続ける
            for event in pygame.event.get():            #pygameのイベントを繰り返しで処理する
                if event.type == QUIT:                   #ウインドウの×ボタンをクリックしたら
                    pygame.quit()                        #pygameモジュールの初期化を解除
                    sys.exit()                        #プログラムを終了する
            self.tmr += 1
            self.cvs.update_canvas(self)
            key = pygame.key.get_pressed()  #keyに全てのキーの状態代入
            key = list(key)
            right ,left = self.direction_change()
            self.manage_game(key,right,left)
            pygame.display.update()  #画面を更新する
            clock.tick(60)  #フレームレートを指定

    def manage_game(self, key,right,left):
        '''
            indexの説明
            0 => タイトル画面
            1 => カウントダウン時
            2 => レース中
            3 => ゴール時
            4 => 車種選択の時
            5 => モード選択の時
            6 => 場所選択の時
            7 => BGM選択の時
            8 => 画像撮影
        '''       

        if self.idx == 0:                                                     #idxが0(タイトル画面)のとき
            self.cvs.screen.blit(self.img_title, [120, 120])  #タイトルロゴを表示
            self.cvs.draw_text("[C] Select your car", 400, 320, C.WHITE, self.cvs.fnt_m)  #[S] Select your car の文字を表示
            self.cvs.draw_text("[L] Select location",400,360,C.WHITE,self.cvs.fnt_m)
            self.cvs.draw_text("[G] Select BGM",400,400,C.WHITE,self.cvs.fnt_m)
            self.cvs.draw_text("[M] Select mode",400,440,C.WHITE,self.cvs.fnt_m)
            self.p1.move_player(self.tmr, self.laps) #プレイヤーの車をただ動かすだけ
            self.com.move_car(1, self.tmr)  #コンピュータの車を動かす
            
            if key[K_c] != 0:                                               #Sキーが押されたら         
                self.idx = 4                                                         #idxを4にして車種選択に移行
            if key[K_m] != 0:                                               #Mキーが押されたら
                self.idx = 5                                                    #idxを5にしてモード選択に移行
            if key[K_l] != 0:                                               #Lキーが押されたら
                self.idx = 6                                                    #idxを6にして場所選択に移行
            if key[K_g] != 0:                                               #Lキーが押されたら
                self.idx = 7                                                    #idxを6にして場所選択に移行

        if self.idx == 1:  #idxが1(カウントダウン)のとき
            time_c = time.time()
            time_cd = 3 - int(time_c - self.time)
            self.music_play()
            self.cvs.draw_text(str(time_cd),400,240,C.YELLOW,self.cvs.fnt_l)
            if time_cd <= 0 :  # カウントダウンが終了したら
                self.idx = 2  #idxを2にしてレースへ                
                self.time = time.time()              #このときの時刻を計算
                self.tmr = 0
            if self.mymode == 1:  #multiplaymodeなら
                #オンライン通信にて敵位置取得＆自分位置送信
                self.multiGame = self.n.send(self.p1)
                #self.cvs.draw_rival(self,screen)  # 対戦相手の描画

        if self.idx == 2:  #idxが2(レース中)のとき
            time_race = time.time()
            self.elapsed_time = time_race - self.time
            self.music_pause(key)

            if self.tmr < 60:  #60フレームの間だけ
                self.cvs.draw_text("Go!", 400, 240, C.RED, self.cvs.fnt_l)  #GO!と表示 
            
            self.music_play()
            self.rec = self.rec + 1 / 60  #走行時間をカウント
            self.p1.drive_car(key, self, self.cvs,right,left) #プレイヤーの車を動かせるように
            
            self.com.move_car(1, self.tmr)  #コンピュータの車を動かす
            self.collision_judge(1)  #衝突判定
            if self.mymode == 1:  #multiplaymodeなら
                #オンライン通信にて敵位置取得＆自分位置送信
                self.multiGame = self.n.send(self.p1)
                #self.cvs.draw_rival(self,screen) # 対戦相手の描画


        if self.idx == 3:              #idxが3(ゴール)のとき
            self.music_play()
            self.cvs.draw_text("GOAL!", 400, 240, C.GREEN, self.cvs.fnt_l)  #GOAL!と表示 
            self.p1.spd = self.p1.spd * 0.96 #プレイヤーの車の速度を落とす
            self.p1.y = self.p1.y + self.p1.spd/100 #コース上を進ませる
            self.com.move_car(1,self.tmr)                    #コンピュータの車を動かす
            if self.tmr > 60*5:                        #8秒経過したら
                self.laps = 0
                self.elapsed_time = 0
                self.idx = 0                                 #idxを0にしてタイトルに戻る

        if self.idx == 4:                                                      #idxが4(車種選択)のとき
            self.tmr, self.laps = self.p1.move_player(self.tmr, self.laps)               #プレイヤーの車を動かす                                   #プレイヤーの車をただ動かすだけ
            self.com.move_car(1, self.tmr)  #コンピュータの車を動かす
            self.car_select(key)

        if self.idx == 5:  #idxが5(モード選択)のとき
            self.tmr, self.laps = self.p1.move_player(self.tmr, self.laps)               #プレイヤーの車を動かす                                   #プレイヤーの車をただ動かすだけ
            self.com.move_car(1,self.tmr)                                                #コンピュータの車を動かす
            self.mode_select(self.cvs.screen, key)
        
        if self.idx == 6:
            self.tmr, self.laps = self.p1.move_player(self.tmr, self.laps)               #プレイヤーの車を動かす                                   #プレイヤーの車をただ動かすだけ
            self.com.move_car(1,self.tmr)                                                #コンピュータの車を動かす
            self.locate_select(self.cvs.screen, key)
            
        if self.idx == 7:
            self.tmr, self.laps = self.p1.move_player(self.tmr, self.laps)               #プレイヤーの車を動かす                                   #プレイヤーの車をただ動かすだけ
            self.com.move_car(1,self.tmr)                                                #コンピュータの車を動かす
            self.bgm_select(self.cvs.screen, key)

    def direction_change(self):
        #バウンディングボックス作成
        while self.idx == 8:
            self.kcf.make_bbox()
            self.idx = 0#写真撮影を終了

        #顔の位置を車両の移動に変換
        right = int(self.kcf.tracking_face()[0])
        left = int(self.kcf.tracking_face()[1])
        # print("RIGHT:{},LEFT:{}".format(right,left))
        return right,left

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


    def car_select(self, key):
        self.cvs.draw_text("Select your car",400,160,C.WHITE,self.cvs.fnt_m)      #Select your car を表示
        for i in range(3):
            x = 160+240*i                                                       #xに選択用の枠のx座標を代入
            y = 300                                                             #yに選択用の枠のy座標を代入
            col = C.GRAY                                                       #colにBLACkを代入
            if i == self.mycar:                                                    #選択している車種なら
                col = (0,128,255)                                                   #colに明るい青の値を代入
            pygame.draw.rect(self.cvs.screen,col,[x-100,y-80,200,200])                   #colの色で枠を描く
            self.cvs.draw_text("["+str(i+1)+"]",x,y-50,C.WHITE,self.cvs.fnt_m)        #[n]の文字を表示
            self.cvs.screen.blit(self.img_car[3+i*7],[x-100,y-20])                       #それぞれの車を描画
        self.cvs.draw_text("[Enter] OK!",400,440,C.GREEN,self.cvs.fnt_m)          #[Enter] OK! を表示
        if key[K_1] == 1:                                                   #1キーが押されたら
            self.mycar = 0                                                         #mycarに0を代入(赤い車)
        if key[K_2] == 1:                                                   #2キーが押されたら
            self.mycar = 1                                                         #mycarに1を代入(青い車)
        if key[K_3] == 1:                                                   #3キーが押されたら
            self.mycar = 2                                                         #mycarに2を代入(黄色の車)
        if key[K_RETURN] == 1:                                              #Enterキーが押されたら
            self.idx = 0                                                           #idxを0にしてタイトル画面に戻る


    def mode_select(self, bg, key):
        self.cvs.draw_text("Select mode",400,160,C.WHITE,self.cvs.fnt_m)          #Select mode を表示
        for i in range(2):                                                  #繰り返しで
            x = 200+400*i                                                       #xに選択用の枠のx座標を代入
            y = 300                                                             #yに選択用の枠のy座標を代入
            col = C.BLACK                                                       #colにBLACkを代入
            if i == self.mymode:                                                    #選択している車種なら
                col = (0,128,255)                                                   #colに明るい青の値を代入
            pygame.draw.rect(bg,col,[x-120,y-120,240,240])                   #colの色で枠を描く
            self.cvs.draw_text("["+str(i+1)+"]",x,y-90,C.WHITE,self.cvs.fnt_m)        #[n]の文字を表示
            if i == 0:
                self.cvs.draw_text("Single play",x,y-40,C.WHITE,self.cvs.fnt_m)
            if i == 1:
                self.cvs.draw_text("Multi play",x,y-40,C.WHITE,self.cvs.fnt_m)
            
            bg.blit(self.img_mode[i],[x-100,y-10])                       #それぞれの車を描画

        self.cvs.draw_text("[Enter] Start game", 400, 460, C.GREEN, self.cvs.fnt_m)  #[Enter] OK! を表示
        self.cvs.draw_text("[B] Back to title", 400, 540, C.WHITE, self.cvs.fnt_m)  #[Enter] OK! を表示
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
                self.laps = 0  #周回数を0に
                self.rec = 0  #走行時間を0に
                self.recbk = 0  #ラップタイム計算用の変数を0に
                for i in range(self.laps):  #繰り返しで
                    self.laptime[i] = "0'00.00"  #ラップタイムを0'00.00に
            if self.mymode == 1:  #multiモードが選択されたら
                self.n = Network()
                self.player = int(self.n.getP()) # プレイヤーNumをGet
                print("You are player", self.player)
                if self.player == 0:
                    self.p1 = Player(300, 0)
                elif self.player == 1:
                    self.p1 = Player(500, 0)
                self.time = time.time()  #このときの時刻を記録
                self.laps = 0  #周回数を0に
                self.rec = 0  #走行時間を0に
                self.recbk = 0  #ラップタイム計算用の変数を0に
                run = True
                while run:
                    try:
                        self.multiGame = self.n.send(self.p1)  # Game object全てが戻ってくる
                    except:
                        run = False
                        print("Couldn't get game")
                        break
                    if not (self.multiGame.connected()):  # 1台のみ接続中
                        print("waiting for opponent")
                        self.cvs.draw_text("Waiting for rival...", 400, 160, C.WHITE, self.cvs.fnt_m)
                        pygame.display.update()
                    else:  # 両者が繋がったら
                        print("Game Id is", self.multiGame.id)
                        self.idx = 1  # カウントダウンフェーズに移行
                        break            

                for i in range(self.laps):  #繰り返しで
                    self.laptime[i] = "0'00.00"  #ラップタイムを0'00.00に


        if key[K_b] != 0:
            self.idx = 0   #タイトル画面に戻る

    def locate_select(self, bg, key):
        self.cvs.draw_text("Select location", 400, 160, C.WHITE, self.cvs.fnt_m)  #Select location を表示
        for i in range(2):
            x = 200 + 400 * i  #xに選択用の枠のx座標を代入
            y = 300  #yに選択用の枠のy座標を代入
            col = C.BLACK  #colにBLACkを代入
            if i == self.mylocation:  #選択している車種なら    
                col = (0, 128, 255)  #colに明るい青の値を代入    
            pygame.draw.rect(bg, col, [x - 120, y - 120, 240, 240])  #colの色で枠を描く
            bg.blit(self.img_location[i], [x - 100, y - 100])  #それぞれの場所を描画
            self.cvs.draw_text("["+str(i+1)+"]",x,y-90,C.WHITE,self.cvs.fnt_m)        #[n]の文字を表示
            if i == 0:
                self.cvs.draw_text("Tokyo",x,y-40,C.WHITE,self.cvs.fnt_m)
            if i == 1:
                self.cvs.draw_text("Space",x,y-40,C.WHITE,self.cvs.fnt_m)
            
            #bg.blit(self.img_location[i],[x-100,y-100])                       #それぞれの場所を描画

        self.cvs.draw_text("[Enter] OK!",400,460,C.GREEN,self.cvs.fnt_m)          #[Enter] OK! を表示
        if key[K_1] == 1:
            self.mylocation = 0  #mylocationに0を代入(Tokyo)
        if key[K_2] == 1: #2キーが押されたら
            self.mylocation = 1 #mylocationに1を代入(Space)
        
        if key[K_RETURN] != 0: 
            self.idx = 0  #タイトル画面に戻る

    def bgm_select(self, bg, key):
        self.cvs.draw_text("Select BGM", 400, 160, C.WHITE, self.cvs.fnt_m)  #Select location を表示
        for i in range(3):
            x = 160                                                       #xに選択用の枠のx座標を代入
            y = 250+40*i                                                             #yに選択用の枠のy座標を代入
            col = C.WHITE                                                       #colにBLACkを代入
            if i == self.mybgm:                                                    #選択している車種なら
                col = (0,128,255)                                                   #colに明るい青の値を代入
            self.cvs.draw_text("["+str(i+1)+"] : ",x,y,col,self.cvs.fnt_m)
            self.cvs.draw_text(self.bgm_race[i],x+250,y,col,self.cvs.fnt_m)
        self.cvs.draw_text("[Enter] OK!",400,440,C.GREEN,self.cvs.fnt_m)          #[Enter] OK! を表示
        if key[K_1] == 1:                                                   #1キーが押されたら
            self.mybgm = 0                                                         #mycarに0を代入(赤い車)
        if key[K_2] == 1:                                                   #2キーが押されたら
            self.mybgm = 1                                                         #mycarに1を代入(青い車)
        if key[K_3] == 1:                                                   #3キーが押されたら
            self.mybgm = 2                                                         #mycarに2を代入(黄色の車)
        if key[K_RETURN] == 1:                                              #Enterキーが押されたら
            self.idx = 0                                                           #idxを0にしてタイトル画面に戻る

    def load_image(self): #画像の読み込み
        self.img_title = pygame.image.load("image_pr/title_sd.png").convert_alpha()    #タイトルロゴ
        #self.img_bg = pygame.image.load("image_pr/tokyo_1.jpg").convert()            #背景(空と地面の絵)
        self.img_bg = [
            pygame.image.load("image_pr/tokyo_3.jpg").convert(),
            pygame.image.load("image_pr/space_3.jpg").convert()
        ]

        self.img_sea = pygame.image.load("image_pr/sea.png").convert_alpha()    #海
        self.img_obj = [
            None,                                                          #オブジェクト名との整合性をとるためにNoneを入れる
            pygame.image.load("image_pr/building_1.jpg").convert_alpha(),       #ビル画像1
            pygame.image.load("image_pr/building_2.png").convert_alpha(),       #ビル画像2
            pygame.image.load("image_pr/mercury_1.png").convert_alpha(),        #水星
            pygame.image.load("image_pr/venus_1.png").convert_alpha()        #金星
        ]
        self.img_car = [
            pygame.image.load("image_pr/car_41.png").convert_alpha(),       #車(左3)_赤
            pygame.image.load("image_pr/car_41.png").convert_alpha(),       #車(左2)
            pygame.image.load("image_pr/car_42.png").convert_alpha(),       #車(左1)
            pygame.image.load("image_pr/car_43.png").convert_alpha(),       #車(正面)
            pygame.image.load("image_pr/car_44.png").convert_alpha(),       #車(右1)
            pygame.image.load("image_pr/car_45.png").convert_alpha(),       #車(右2)
            pygame.image.load("image_pr/car_45.png").convert_alpha(),       #車(右3)
            pygame.image.load("image_pr/car_30.png").convert_alpha(),       #車(左3)_青
            pygame.image.load("image_pr/car_31.png").convert_alpha(),       #車(左2)
            pygame.image.load("image_pr/car_32.png").convert_alpha(),       #車(左1)
            pygame.image.load("image_pr/car_33.png").convert_alpha(),       #車(正面)
            pygame.image.load("image_pr/car_34.png").convert_alpha(),       #車(右1)
            pygame.image.load("image_pr/car_35.png").convert_alpha(),       #車(右2)
            pygame.image.load("image_pr/car_36.png").convert_alpha(),       #車(右3)
            pygame.image.load("image_pr/car_51.png").convert_alpha(),       #車(左3)_黄色
            pygame.image.load("image_pr/car_51.png").convert_alpha(),       #車(左2)
            pygame.image.load("image_pr/car_52.png").convert_alpha(),       #車(左1)
            pygame.image.load("image_pr/car_53.png").convert_alpha(),       #車(正面)
            pygame.image.load("image_pr/car_54.png").convert_alpha(),       #車(右1)
            pygame.image.load("image_pr/car_55.png").convert_alpha(),       #車(右2)
            pygame.image.load("image_pr/car_55.png").convert_alpha()        #車(右3)
        ]
        
        self.img_mode = [
            pygame.image.load("image_pr/singlemode.png").convert_alpha(),
            pygame.image.load("image_pr/multimode.png").convert_alpha()
        ]

        self.img_location = [
            pygame.image.load("image_pr/tokyo_2.jpg").convert(),
            pygame.image.load("image_pr/space_2.png").convert(),
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
                pygame.mixer.music.load(self.bgm_race[self.mybgm])                          #BGMを読み込み 
                pygame.mixer.music.set_volume(0.2)                                   #音を小さくして
                pygame.mixer.music.play(-1)          
            
        if self.idx == 3:   #ゴール画面
            if self.tmr == 1:                                                      #tmrが1なら
                #pygame.mixer.music.stop()                                             #bgmを停止
                pygame.mixer.music.fadeout(1000)
            if self.tmr == 30:                                                     #tmrが30になったら
                pygame.mixer.music.load("sound_pr/goal.ogg")                          #BGMを読み込み
                pygame.mixer.music.set_volume(0.2)                                   #音を小さくして
                pygame.mixer.music.play(0)     
        if self.idx == 4:   #車種選択画面
            pass
        if self.idx == 5:   #モード選択画面
            pass   

    def music_pause(self,key):
        if pygame.mixer.music.get_busy() == True:
            if key[K_F1] == 1:
                pygame.mixer.music.pause()
            if key[K_F2] == 1:
                pygame.mixer.music.unpause()

        
    def load_bgm(self):
        self.bgm_race = [
            "sound_pr/yoasobi.mp3",
            "sound_pr/kanzen.mp3",
            "sound_pr/ultrasoul.mp3"
        ]
    
    def load_sound(self):
        self.se_crash = pygame.mixer.Sound("sound_pr/crash.ogg")   #SE(衝突音)の読み込み
        self.se_crash.set_volume(0.2)                              #衝突音が大きすぎたので小さくする


if __name__ == '__main__':
    g = Game()
    g.run()

 