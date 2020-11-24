import pygame
from pygame.locals import *  #pygame.定数の記述の省略
import Const as C


class Canvas:
    def update_canvas(self, game, curve, updown, vertical, screen, object_left, object_right, fnt_s, fnt_m, fnt_l):
        #描画用の道路のX座標と路面の高低を計算
        di = 0                                                    #道が曲がる向きを計算する変数
        ud = 0                                                    #道の起伏を計算する変数
        board_x = [0]* C.BOARD                                      #板のx座標を計算するためのリスト
        board_ud = [0]* C.BOARD                                     #板の工程を計算するためのリスト
        for i in range(C.BOARD):
            di += curve[int(game.p1.y+i) % C.CMAX]                      #カーブデータからの道の曲がりを計算
            ud += updown[int(game.p1.y+i) % C.CMAX]                     #起伏データから起伏を計算
            board_x[i] = 400 - C.BOARD_W[i]*game.p1.x/800 + di/2        #板のx座標を計算し代入
            board_ud[i] = ud/30                                      #板の高低を計算し代入
        

        horizon = 400 + int(ud/3)                                 #地平線のy座標を計算しhorizonに代入
        sy = horizon                                              #道路を描き始めるy座標をsyに代入

        vertical = vertical - int(game.p1.spd*di/8000)             #背景の垂直位置を計算
        #背景の垂直位置
        if vertical < 0:                                           #それが0未満になったら
            vertical += 800                                          #800を足す
        if vertical >= 800:                                        #800以上になったら
            vertical -= 800                                          #800を引く

        #フィードの描画
        screen.fill((0,0,0)) #上空の色                           #指定の色で画面を塗りつぶす
        screen.blit(game.img_bg,[vertical-800,horizon-500])             #空と地面の画像を描画(左側)
        screen.blit(game.img_bg,[vertical,horizon-500])                 #空と地面の画像を描画(右側)
        #screen.blit(game.img_sea,[board_x[C.BOARD-1]-780,sy])             #左手奥の海を描画

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
            if int(game.p1.y+i) % C.CMAX == game.p1.PLself + 10:                 #ゴールの位置なら
                col = (192,0,0)                                         #赤線の色の値を代入
            side_w = uw * 0.5

            pygame.draw.polygon(screen,col,[[ux,uy],[ux+uw,uy],[bx+bw,by],[bx,by]])   #道路の板を描く
            pygame.draw.polygon(screen,C.BLACK,[[ux,uy],[bx,by],[bx-side_w,by],[ux-side_w,uy]])   #道路脇の板を描く(左)
            pygame.draw.polygon(screen,C.BLACK,[[ux+uw,uy],[ux+uw+side_w,uy],[bx+bw+side_w,by],[bx+bw,by]])   #道路脇の板を描く(右)

            if int(game.p1.y+i)%10 <= 4:  #左右の黄色線を描画
                pygame.draw.polygon(screen,C.YELLOW,[[ux,uy],[ux+uw*0.02,uy],[bx+bw*0.02,by],[bx,by]])      #左
                pygame.draw.polygon(screen,C.YELLOW,[[ux+uw*0.98,uy],[ux+uw,uy],[bx+bw,by],[bx+bw*0.98,by]])   #右

            if int(game.p1.y+i)%20 <= 10:   #白線を描画
                pygame.draw.polygon(screen,C.WHITE,[[ux+uw*0.24,uy],[ux+uw*0.26,uy],[bx+bw*0.26,by],[bx+bw*0.24,by]])  #左
                pygame.draw.polygon(screen,C.WHITE,[[ux+uw*0.49,uy],[ux+uw*0.51,uy],[bx+bw*0.51,by],[bx+bw*0.49,by]])  #中央
                pygame.draw.polygon(screen,C.WHITE,[[ux+uw*0.74,uy],[ux+uw*0.76,uy],[bx+bw*0.76,by],[bx+bw*0.74,by]])  #右


            scale = 1.5*C.BOARD_W[i]/C.BOARD_W[0]    #道路横の物体のスケールを計算
            obj_l = object_left[int(game.p1.y+i)%C.CMAX]   #道路左の物体
            
            if obj_l == 2: #ヤシの木
                self.draw_obj(screen,game.img_obj[obj_l],ux-uw*0.2,uy,scale)
            """
            if obj_l == 3: #ヨット
                self.draw_obj(screen,game.img_obj[obj_l],ux-uw*0.5,uy,scale)
            if obj_l == 9: #海
                screen.blit(game.img_sea,[ux-uw*0.5-780,uy])
            """

            obj_r = object_right[int(game.p1.y+i)%C.CMAX]  #道路右の物体
              #看板はいらないため描画しない
            if obj_r == 1:  #看板
                self.draw_obj(screen,game.img_obj[obj_r],ux+uw*1.2,uy,scale)
            

            for c in range(1,C.CAR_NUM):                                      #繰り返しで
                if int(game.com.y[c])%C.CMAX == int(game.p1.y+i)%C.CMAX:          #その板にCOMカーがあるかどうか調べ
                    lr = int(4*(game.p1.x-game.com.x[c])/800)                 #プレイヤーから見たCOMカーの向きを計算し
                    if lr < -3:                                         #-3より小さいなら-3で
                        lr = -3
                    if lr > 3:                                          #3より大きいなら3で
                        lr = 3
                    self.draw_obj(screen,game.img_car[(c%3)*7+3+lr],ux+game.com.x[c]*C.BOARD_W[i]/800,uy,0.05+C.BOARD_W[i]/C.BOARD_W[0])

                
            if i == game.p1.PLself: #PLAYERカー                                                                           #プレイヤーの車の位置なら
                self.draw_shadow(screen, ux + game.p1.x * C.BOARD_W[i] / 800, uy, 200 * C.BOARD_W[i] / C.BOARD_W[0])  #車の影を描く
                self.draw_obj(screen, game.img_car[3 + game.p1.lr + game.mycar*7], ux + game.p1.x * C.BOARD_W[i] / 800, uy, 0.05+ C.BOARD_W[i] / C.BOARD_W[0])  #プレイヤーの車を描く
        
        #右側の部分の表示
        pygame.draw.rect(screen,C.WHITE,[800,0,300,600]) 
        self.make_map(screen)
        self.map_pl(game, screen, 900)

        
        self.draw_text(screen,str(int(game.p1.spd))+"km/h",680,30,C.RED,fnt_m)            #速度を表示
        if game.idx != 3:
            self.draw_text(screen,"lap {}/{}".format(game.laps+1,C.LAPS),100,30,C.WHITE,fnt_m)     #周回数を表示
        if game.idx == 3:
            self.draw_text(screen,"lap {}/{}".format(game.laps,C.LAPS),100,30,C.WHITE,fnt_m)     #補正した周回数を表示
        self.draw_text(screen,"time "+game.p1.time_str(game.rec),100,80,C.GREEN,fnt_s)             #タイムを表示
        for i in range(game.laps):                                                  #繰り返しで
            self.draw_text(screen, game.laptime[i], 80, 130 + 40 * i, C.YELLOW, fnt_s)  #ラップタイムを表示

    
    def make_map(self,bg):
        fnt_s = pygame.font.Font(None,20)    #小さい文字
        pygame.draw.line(bg,C.BLACK,[850,500],[950,500],3)   #スタートラインの描画
        pygame.draw.line(bg,C.BLACK,[850,100],[950,100],3)     #ゴールラインの描画 
        txt_s = fnt_s.render("Start",True,C.BLACK)           #Startの記述
        txt_g = fnt_s.render("Goal",True,C.BLACK)            #Goalの記述
        bg.blit(txt_s,[810,490])
        bg.blit(txt_g,[810,90])
        for i in range(1,C.LAPS):    #ラップに対応したラインの描画
            pygame.draw.line(bg,C.BLACK,[850,100+int(i*400/C.LAPS)],[950,100+int(i*400/C.LAPS)],1)
            txt_lap = fnt_s.render("{}/{}".format((C.LAPS-i),C.LAPS),True,C.BLACK)
            bg.blit(txt_lap,[810,100+int(i*400/C.LAPS)-10])


    def map_pl(self, game, bg ,x):
        pygame.draw.line(bg,C.BLACK,[x,500],[x,100],1)      #中心線の描画
        fnt_s = pygame.font.Font(None,20)    #小さい文字
        map_car_col = C.RED                 #車種によって円の色を変える
        if game.mycar == 0:
            map_car_col = C.RED
        if game.mycar == 1:
            map_car_col = C.BLUE
        if game.mycar == 2:
            map_car_col = C.YELLOW
        
        y = 100 + (C.CMAX * (C.LAPS - game.laps) - game.p1.y) * 400 / (C.CMAX * C.LAPS) #マップ上のy座標を計算
        pygame.draw.circle(bg, map_car_col, [x, int(y)], 8, 0) #マップ上に円を描画

        pl = ""           #プレイヤーがどちらなのかを入れる変数
        if game.p1 == game.p1: # ??どういう意味？
            pl = "1p"
        txt_pl = fnt_s.render(pl,True,C.BLACK)
        bg.blit(txt_pl,[910,int(y)-10])


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

