import pygame
import sys
from math import sin,radians
import random
from pygame.locals import *  #pygame.定数の記述の省略
import Const as C
from player import Player
from computer import Computer


class Game:
    def __init__(self):
        # self.game_mode = game_mode # game_mode 1:1人プレイ, 2人プレイ
        self.p1 = Player() # Player1定義
        # self.p2 = Player() # Player2 定義
        # self.net = Network()  # Online機能のロード
        self.com = Computer()
        # Parameters(Varaible)
        self.idx = 0
        self.tmr = 0                           #タイマーの変数
        self.laps = 0                          #何周目かを管理する変数
        self.rec = 0                           #走行時間を測る変数
        self.recbk = 0                         #ラップタイム計算用の変数
        self.laptime = ["0'00.00"] * C.LAPS #ラップタイム表示用のリスト
        self.mycar = 0                         #車選択用の変数

    def collision_judge(self,cs):
        if self.idx == 2:
            for i in range(cs,C.CAR_NUM):
                cx = self.com.x[i]-self.p1.x                                        #プレイヤーの車との横方向の距離
                cy = self.com.y[i]-(self.p1.y+self.p1.PLself) % C.CMAX                         #プレイヤーの車とのコース上の距離
                if -100 <= cx and cx <= 100 and -10 <= cy and cy <= 10:       #それらがこの範囲内なら
                    #衝突時の座標変化、速度の入れ替えと減速
                    self.p1.x -= cx/4                                          #プレイヤーの車を横に移動
                    self.com.x[i] += cx/4                                          #コンピュータの車を横に移動
                    self.p1.spd, self.com.spd[i] = self.com.spd[i]*0.3, self.p1.spd*0.3   #2つの車の速度を入れ替え、減速する
                    self.se_crash.play()                                           #衝突音を出力する
        

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
            self.update_canvas(curve, updown, vertical, screen, object_left, object_right, fnt_s, fnt_m, fnt_l)
            key = pygame.key.get_pressed()                       #keyに全てのキーの状態代入
            self.manage_game(key, curve, screen, fnt_s, fnt_m, fnt_l)
            pygame.display.update()                      #画面を更新する
            clock.tick(60)                               #フレームレートを指定

    def manage_game(self, key, curve, screen, fnt_s, fnt_m, fnt_l):
        if self.idx == 0:                                                     #idxが0(タイトル画面)のとき
            screen.blit(self.img_title,[120,120])                               #タイトルロゴを表示
            self.draw_text(screen,"[A] Start game",400,320,C.WHITE,fnt_m)            #[A] Start game の文字を表示
            self.draw_text(screen,"[S] Select your car",400,400,C.WHITE,fnt_m)       #[S] Select your car の文字を表示
            self.p1.move_player(self.tmr, self.laps) #プレイヤーの車をただ動かすだけ
            self.com.move_car(1, self.tmr)                                                #コンピュータの車を動かす
            if key[K_a] != 0:                                                   #Aキーが押されたら
                self.p1.__init__()                                                   #プレイヤーの車を初期化
                self.com.__init__()                                                  #コンピュータの車を初期化
                self.idx = 1                                                            #idxを1にしてカウントダウンに
                self.tmr = 0                                                            #タイマーを0に
                self.laps = 0                                                    #周回数を0に
                self.rec = 0                                                     #走行時間を0に
                self.recbk = 0                                                   #ラップタイム計算用の変数を0に
                for i in range(self.laps):                                       #繰り返しで
                    self.laptime[i] = "0'00.00"                                      #ラップタイムを0'00.00に
            if key[K_s] != 0:                                               #Sキーが押されたら         
                self.idx = 4                                                         #idxを4にして車種選択に移行

        if self.idx == 1:                                                    #idxが1(カウントダウン)のとき
            n = 3-int(self.tmr/60)                                                 #カウントダウンの数を計算しnに代入
            self.draw_text(screen,str(n),400,240,C.YELLOW,fnt_l)                #その数を表示
            if self.tmr == 179:                                                    #tmrが179になったら
                pygame.mixer.music.load("sound_pr/bgm.ogg")                          #BGMを読み込み
                pygame.mixer.music.set_volume(0.2)                                   #音を小さくして
                pygame.mixer.music.play(-1)                                          #無限ループで出力
                self.idx = 2                                                              #idxを2にしてレースへ
                self.tmr = 0                                                              #tmrを0にする

        if self.idx == 2:                                                    #idxが2(レース中)のとき
            if self.tmr < 60:                                                      #60フレームの間だけ
                self.draw_text(screen,"Go!",400,240,C.RED,fnt_l)                     #GO!と表示
            self.rec = self.rec + 1/60                                                 #走行時間をカウント
            self.p1.drive_car(key, curve, self.laptime, self.laps, self.rec, self.recbk, self.tmr)                                       #プレイヤーの車を動かせるように
            self.com.move_car(1, self.tmr)                                                #コンピュータの車を動かす
            self.collision_judge(1)                                             #衝突判定

        if self.idx == 3:                                                    #idxが3(ゴール)のとき
            if self.tmr == 1:                                                      #tmrが1なら
                pygame.mixer.music.stop()                                             #bgmを停止
                #self.laps = self.laps - 1
            if self.tmr == 30:                                                     #tmrが30になったら
                pygame.mixer.music.load("sound_pr/goal.ogg")                          #ゴール音を読み込み
                pygame.mixer.music.set_volume(0.2)                                    #音を小さくして
                pygame.mixer.music.play(0)                                            #1回だけ出力
            self.draw_text(screen,"GOAL!",400,240,C.GREEN,fnt_l)                #GOAL!と表示       
            self.p1.spd = self.p1.spd*0.96                                      #プレイヤーの車の速度を落とす
            self.p1.y = self.p1.y + self.p1.spd/100                             #コース上を進ませる
            self.com.move_car(1)                                                #コンピュータの車を動かす
            if self.tmr > 60*8:                                                    #8秒経過したら
                self.laps = 0
                self.idx = 0                                                             #idxを0にしてタイトルに戻る

        if self.idx == 4:                                                      #idxが4(車種選択)のとき
            self.p1.move_player()                                               #プレイヤーの車をただ動かすだけ
            self.com.move_car(1)                                                #コンピュータの車を動かす
            self.draw_text(screen,"Select your car",400,160,C.WHITE,fnt_m)      #Select your car を表示
            for i in range(3):                                                  #繰り返しで
                x = 160+240*i                                                       #xに選択用の枠のx座標を代入
                y = 300                                                             #yに選択用の枠のy座標を代入
                col = C.BLACK                                                       #colにBLACkを代入
                if i == self.mycar:                                                    #選択している車種なら
                    col = (0,128,255)                                                   #colに明るい青の値を代入
                pygame.draw.rect(screen,col,[x-100,y-80,200,160])                   #colの色で枠を描く
                self.draw_text(screen,"["+str(i+1)+"]",x,y-50,C.WHITE,fnt_m)        #[n]の文字を表示
                screen.blit(self.img_car[3+i*7],[x-100,y-20])                       #それぞれの車を描画
            self.draw_text(screen,"[Enter] OK!",400,440,C.GREEN,fnt_m)          #[Enter] OK! を表示
            if key[K_1] == 1:                                                   #1キーが押されたら
                self.mycar = 0                                                         #mycarに0を代入(赤い車)
            if key[K_2] == 1:                                                   #2キーが押されたら
                self.mycar = 1                                                         #mycarに1を代入(青い車)
            if key[K_3] == 1:                                                   #3キーが押されたら
                self.mycar = 2                                                         #mycarに2を代入(黄色の車)
            if key[K_RETURN] == 1:                                              #Enterキーが押されたら
                self.idx = 0                                                           #idxを0にしてタイトル画面に戻る

    def update_canvas(self, curve, updown, vertical, screen, object_left, object_right, fnt_s, fnt_m, fnt_l):
        #描画用の道路のX座標と路面の高低を計算
        di = 0                                                    #道が曲がる向きを計算する変数
        ud = 0                                                    #道の起伏を計算する変数
        board_x = [0]* C.BOARD                                      #板のx座標を計算するためのリスト
        board_ud = [0]* C.BOARD                                     #板の工程を計算するためのリスト
        for i in range(C.BOARD):
            di += curve[int(self.p1.y+i) % C.CMAX]                      #カーブデータからの道の曲がりを計算
            ud += updown[int(self.p1.y+i) % C.CMAX]                     #起伏データから起伏を計算
            board_x[i] = 400 - C.BOARD_W[i]*self.p1.x/800 + di/2        #板のx座標を計算し代入
            board_ud[i] = ud/30                                      #板の高低を計算し代入
        

        horizon = 400 + int(ud/3)                                 #地平線のy座標を計算しhorizonに代入
        sy = horizon                                              #道路を描き始めるy座標をsyに代入

        vertical = vertical - int(self.p1.spd*di/8000)             #背景の垂直位置を計算
        #背景の垂直位置
        if vertical < 0:                                           #それが0未満になったら
            vertical += 800                                          #800を足す
        if vertical >= 800:                                        #800以上になったら
            vertical -= 800                                          #800を引く

        #フィードの描画
        screen.fill((0,56,255)) #上空の色                           #指定の色で画面を塗りつぶす
        screen.blit(self.img_bg,[vertical-800,horizon-400])             #空と地面の画像を描画(左側)
        screen.blit(self.img_bg,[vertical,horizon-400])                 #空と地面の画像を描画(右側)
        screen.blit(self.img_sea,[board_x[C.BOARD-1]-780,sy])             #左手奥の海を描画

        #描画用データを基に道路を描く
        for i in range(C.BOARD-1,0,-1):                              #繰り返しで道路の板を描いていく
            ux = board_x[i]                                        #台形の上底のx座標をuxに代入
            uy = sy - C.BOARD_UP[i]*board_ud[i]                      #上底のy座標をuyに代入
            uw = C.BOARD_W[i]                                        #上底の幅をuwに代入
            sy = sy + C.BOARD_H[i]*(600-horizon)/200                 #台形を描くy座標を次の値にする
            bx = board_x[i-1]                                      #台形の下底のx座標をbxに代入
            by = sy - C.BOARD_UP[i-1]*board_ud[i-1]                  #下底のy座標をbyに代入
            bw = C.BOARD_W[i-1]                                      #下底の幅をbwに代入
            col = (160,160,160)                                    #colに板の色を代入
            if int(self.p1.y+i) % C.CMAX == self.p1.PLself + 10:                 #ゴールの位置なら
                col = (192,0,0)                                         #赤線の色の値を代入
            
            pygame.draw.polygon(screen,col,[[ux,uy],[ux+uw,uy],[bx+bw,by],[bx,by]])   #道路の板を描く

            if int(self.p1.y+i)%10 <= 4:  #左右の黄色線を描画
                pygame.draw.polygon(screen,C.YELLOW,[[ux,uy],[ux+uw*0.02,uy],[bx+bw*0.02,by],[bx,by]])      #左
                pygame.draw.polygon(screen,C.YELLOW,[[ux+uw*0.98,uy],[ux+uw,uy],[bx+bw,by],[bx+bw*0.98,by]])   #右

            if int(self.p1.y+i)%20 <= 10:   #白線を描画
                pygame.draw.polygon(screen,C.WHITE,[[ux+uw*0.24,uy],[ux+uw*0.26,uy],[bx+bw*0.26,by],[bx+bw*0.24,by]])  #左
                pygame.draw.polygon(screen,C.WHITE,[[ux+uw*0.49,uy],[ux+uw*0.51,uy],[bx+bw*0.51,by],[bx+bw*0.49,by]])  #中央
                pygame.draw.polygon(screen,C.WHITE,[[ux+uw*0.74,uy],[ux+uw*0.76,uy],[bx+bw*0.76,by],[bx+bw*0.74,by]])  #右


            scale = 1.5*C.BOARD_W[i]/C.BOARD_W[0]    #道路横の物体のスケールを計算
            obj_l = object_left[int(self.p1.y+i)%C.CMAX]   #道路左の物体
            if obj_l == 2: #ヤシの木
                self.draw_obj(screen,self.img_obj[obj_l],ux-uw*0.05,uy,scale)
            if obj_l == 3: #ヨット
                self.draw_obj(screen,self.img_obj[obj_l],ux-uw*0.5,uy,scale)
            if obj_l == 9: #海
                screen.blit(self.img_sea,[ux-uw*0.5-780,uy])

            obj_r = object_right[int(self.p1.y+i)%C.CMAX]  #道路右の物体
            """  #看板はいらないため描画しない
            if obj_r == 1:  #看板
                self.draw_obj(screen,img_obj[obj_r],ux+uw*1.3,uy,scale)
            """

            for c in range(1,C.CAR_NUM):                                      #繰り返しで
                if int(self.com.y[c])%C.CMAX == int(self.p1.y+i)%C.CMAX:          #その板にCOMカーがあるかどうか調べ
                    lr = int(4*(self.p1.x-self.com.x[c])/800)                 #プレイヤーから見たCOMカーの向きを計算し
                    if lr < -3:                                         #-3より小さいなら-3で
                        lr = -3
                    if lr > 3:                                          #3より大きいなら3で
                        lr = 3
                    self.draw_obj(screen,self.img_car[(c%3)*7+3+lr],ux+self.com.x[c]*C.BOARD_W[i]/800,uy,0.05+C.BOARD_W[i]/C.BOARD_W[0])

                
            if i == self.p1.PLself: #PLAYERカー                                                                           #プレイヤーの車の位置なら
                self.draw_shadow(screen, ux + self.p1.x * C.BOARD_W[i] / 800, uy, 200 * C.BOARD_W[i] / C.BOARD_W[0])  #車の影を描く
                self.draw_obj(screen, self.img_car[3 + self.p1.lr + self.mycar*7], ux + self.p1.x * C.BOARD_W[i] / 800, uy, 0.05+ C.BOARD_W[i] / C.BOARD_W[0])  #プレイヤーの車を描く
        
        #右側の部分の表示
        pygame.draw.rect(screen,C.WHITE,[800,0,300,600]) 
        self.make_map(screen)
        self.map_pl(screen,self.p1,900)

        
        self.draw_text(screen,str(int(self.p1.spd))+"km/h",680,30,C.RED,fnt_m)            #速度を表示
        self.draw_text(screen,"lap {}/{}".format(self.laps+1,self.laps),100,30,C.WHITE,fnt_m)     #周回数を表示
        self.draw_text(screen,"time "+self.p1.time_str(self.rec),100,80,C.GREEN,fnt_s)             #タイムを表示
        for i in range(self.laps):                                                  #繰り返しで
            self.draw_text(screen,self.laptime[i],80,130+40*i,C.YELLOW,fnt_s)                  #ラップタイムを表示

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

    def make_map(self,bg):
        fnt_s = pygame.font.Font(None,20)    #小さい文字
        pygame.draw.line(bg,C.BLACK,[850,500],[950,500],3)   #スタートラインの描画
        pygame.draw.line(bg,C.BLACK,[850,100],[950,100],3)     #ゴールラインの描画 
        txt_s = fnt_s.render("Start",True,C.BLACK)           #Startの記述
        txt_g = fnt_s.render("Goal",True,C.BLACK)            #Goalの記述
        bg.blit(txt_s,[810,490])
        bg.blit(txt_g,[810,90])
        for i in range(1,self.laps):    #ラップに対応したラインの描画
            pygame.draw.line(bg,C.BLACK,[850,100+int(i*400/self.laps)],[950,100+int(i*400/self.laps)],1)
            txt_lap = fnt_s.render("{}/{}".format((self.laps-i),self.laps),True,C.BLACK)
            bg.blit(txt_lap,[810,100+int(i*400/self.laps)-10])


    def map_pl(self,bg,player,x):
        pygame.draw.line(bg,C.BLACK,[x,500],[x,100],1)      #中心線の描画
        fnt_s = pygame.font.Font(None,20)    #小さい文字
        map_car_col = C.RED                 #車種によって円の色を変える
        if self.mycar == 0:
            map_car_col = C.RED
        if self.mycar == 1:
            map_car_col = C.BLUE
        if self.mycar == 2:
            map_car_col = C.YELLOW
        
        y = 100 + (C.CMAX * (C.LAPS - self.laps) - player.y) * 400 / (C.CMAX * C.LAPS) #マップ上のy座標を計算
        pygame.draw.circle(bg, map_car_col, [x, int(y)], 8, 0) #マップ上に円を描画

        pl = ""           #プレイヤーがどちらなのかを入れる変数
        if player == self.p1:
            pl = "1p"
        txt_pl = fnt_s.render(pl,True,C.BLACK)
        bg.blit(txt_pl,[910,int(y)-10])

        
        


    def load_image(self): #画像の読み込み
        self.img_title = pygame.image.load("image_pr/title.png").convert_alpha()    #タイトルロゴ
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
    
    def load_sound(self):
        self.se_crash = pygame.mixer.Sound("sound_pr/crash.ogg")   #SE(衝突音)の読み込み
        self.se_crash.set_volume(0.2)                              #衝突音が大きすぎたので小さくする

    @staticmethod
    def draw_obj(bg, img, x, y, sc):                        #座標とスケールを受け取り、物体を描く関数
        img_rz = pygame.transform.rotozoom(img,0,sc)        #拡大縮小した画像を受け取る
        w = img_rz.get_width()                              #その画像の幅をwに代入
        h = img_rz.get_height()                             #その画像の高さをhに代入
        bg.blit(img_rz,[x-w/2,y-h])                         #画像を描く

    @staticmethod
    def draw_shadow(bg,x,y,siz):                            #車の影を表示する関数
        shadow = pygame.Surface([siz,siz/4])                #描画面(サーフェース)を用意する
        shadow.fill(C.RED)                                    #その描画面を赤で埋めつくす
        shadow.set_colorkey(C.RED)                            #Surfaceの透過色を指定
        shadow.set_alpha(128)                               #Surfaceの透明度を指定
        pygame.draw.ellipse(shadow,C.BLACK,[0,0,siz,siz/4])   #描画面に黒で楕円を描く
        bg.blit(shadow,[x-siz/2,y-siz/4])                   #楕円を描いた描画面をゲーム画面に転送

    @staticmethod
    def draw_text(scrn,txt,x,y,col,fnt):                            #影付きの文字列を表示する関数
        sur = fnt.render(txt,True,C.BLACK)                            #黒で文字列を描いたサーフェースを生成
        x -= sur.get_width()/2                                      #センタリングするためx座標を計算
        y -= sur.get_height()/2                                     #センタリングするためy座標を計算
        scrn.blit(sur,[x+2,y+2])                                    #サーフェースを画面に転送
        sur = fnt.render(txt,True,col)                              #指定色で文字列を描いたサーフェースを作成
        scrn.blit(sur,[x,y])                                        #サーフェースを画面に転送




if __name__ == '__main__':
    g = Game()
    g.run()