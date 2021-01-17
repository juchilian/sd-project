import pygame
import random
from pygame.locals import *  #pygame.定数の記述の省略
import Const as C


class Canvas:
    def __init__(self):
        self.screen = pygame.display.set_mode((1100,600)) #描画面を初期化
        self.fnt_ss = pygame.font.Font(None,20)    #小小さい文字
        self.fnt_s = pygame.font.Font(None,40)    #小さい文字
        self.fnt_m = pygame.font.Font(None,50)    #中くらいの文字
        self.fnt_l = pygame.font.Font(None,120)   #大きい文字
        self.vertical = 0  #背景の横方向の位置を管理する変数
        self.curve = [0] * C.CMAX           #道が曲がる向きを入れるリスト
        self.updown = [0] * C.CMAX          #道の起伏を入れるリスト
        self.object_left = [0]*C.CMAX     #道路左にある物体の番号を入れるリスト
        self.object_right = [0] * C.CMAX  #道路右にある物体の番号を入れるリスト
        self.object_uright = [0] * C.CMAX
        self.object_uleft = [0] * C.CMAX
        self.make_course()
        self.person_SD1 = [random.randint(1,28) for i in range(C.CLEN)]
        self.person_SD2 = [random.randint(1,28) for i in range(C.CLEN)]
        self.person_SD3 = [random.randint(1,28) for i in range(C.CLEN)]
        self.person_SD4 = [random.randint(1,28) for i in range(C.CLEN)]
        self.person_SD5 = [random.randint(1,28) for i in range(C.CLEN)]
        self.person_SD6 = [random.randint(1,28) for i in range(C.CLEN)]
        self.star_sun1 = [random.randint(1,4) for i in range(C.CLEN)]
        self.star_sun2 = [random.randint(5,9) for i in range(C.CLEN)]
        self.star_sun3 = [random.randint(4,9) for i in range(C.CLEN)]
        self.star_sun4 = [random.randint(1,4) for i in range(C.CLEN)]
        self.star_sun5 = [random.randint(5,9) for i in range(C.CLEN)]
        self.star_sun6 = [random.randint(1,7) for i in range(C.CLEN)]
        self.star_sun7 = [random.randint(1,4) for i in range(C.CLEN)]
        self.star_sun8 = [random.randint(5,9) for i in range(C.CLEN)]
        self.star_sun9 = [random.randint(1,9) for i in range(C.CLEN)]
        self.star_sun10 = [random.randint(1,4) for i in range(C.CLEN)]
        self.star_sun11 = [random.randint(5,9) for i in range(C.CLEN)]
        self.star_sun12 = [random.randint(1,9) for i in range(C.CLEN)]
        


    def make_course(self): #コースデータを作る関数 #修正箇所(returnで値の変更を反映)
        for i in range(C.CLEN):
            lr1 = C.DATA_LR[i]                    #カーブデータをlr1に代入   
            lr2 = C.DATA_LR[(i+1)%C.CLEN]           #次のカーブデータをlr2に代入
            ud1 = C.DATA_UD[i]                    #起伏のデータをud1に代入
            ud2 = C.DATA_UD[(i+1)%C.CLEN]           #次の起伏のデータをud2に代入
            for j in range(C.BOARD):
                pos = j + C.BOARD*i                                      #リストの添え字を計算しposに代入
                self.curve[pos]  = lr1*(C.BOARD-j)/C.BOARD + lr2*j/C.BOARD        #道が曲がる向きを計算し代入
                self.updown[pos] = ud1*(C.BOARD-j)/C.BOARD + ud2*j/C.BOARD        #道の起伏を計算し代入
                



    def update_canvas(self, game):
        #描画用の道路のX座標と路面の高低を計算
        di = 0  #道が曲がる向きを計算する変数
        ud = 0  #道の起伏を計算する変数
        board_x = [0] * C.BOARD  #板のx座標を計算するためのリスト
        board_ud = [0] * C.BOARD  #板の工程を計算するためのリスト
        for i in range(C.BOARD):
            di += self.curve[int(game.p1.y + i) % C.CMAX]  #カーブデータからの道の曲がりを計算
            ud += self.updown[int(game.p1.y + i) % C.CMAX]  #起伏データから起伏を計算
            board_x[i] = 400 - C.BOARD_W[i] * game.p1.x / 800 + di / 2  #板のx座標を計算し代入
            board_ud[i] = ud / 30  #板の高低を計算し代入
        

        horizon = 400 + int(ud / 3)  #地平線のy座標を計算しhorizonに代入
        sy = horizon  #道路を描き始めるy座標をsyに代入

        self.vertical = self.vertical - int(game.p1.spd * di / 8000)  #背景の垂直位置を計算

        #フィードの描画
        self.screen.fill((0,0,0)) #上空の色  #指定の色で画面を塗りつぶす
        bg_width = game.img_bg[game.mylocation].get_width()
        bg_height = game.img_bg[game.mylocation].get_height()
        img_otherside = pygame.transform.flip(game.img_bg[game.mylocation],1,0)
        offset_y = 0
        if game.mylocation == 0:
            offset_y = 550
        if game.mylocation == 1:
            offset_y = 800
        if game.mylocation == 2:
            offset_y = 800

        #背景の垂直位置
        
        # if self.vertical < 0:  #それが0未満になったら
        #     self.vertical += 2754  #800を足す
        # if self.vertical >= 2*bg_width:  #800以上になったら
        #     self.vertical -= 2*bg_width  #800を引く
        self.screen.blit(img_otherside,[self.vertical-3*bg_width,horizon-offset_y]) 
        self.screen.blit(game.img_bg[game.mylocation],[self.vertical-2*bg_width,horizon-offset_y]) 
        self.screen.blit(img_otherside,[self.vertical-bg_width,horizon-offset_y]) 
        self.screen.blit(game.img_bg[game.mylocation],[self.vertical,horizon-offset_y])
        self.screen.blit(img_otherside,[self.vertical+bg_width,horizon-offset_y])  
        self.screen.blit(game.img_bg[game.mylocation],[self.vertical+2*bg_width,horizon-offset_y])  
        self.screen.blit(img_otherside,[self.vertical+3*bg_width,horizon-offset_y])  

        self.update_object(game)
        
        
        
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
            scale = 1.5*C.BOARD_W[i]/C.BOARD_W[0]    #道路横の物体のスケールを計算

            if int(game.p1.y+i) % C.CMAX == game.p1.PLself + 10:                 #ゴールの位置なら
                col = (192,0,0)                                         #赤線の色の値を代入
                pygame.draw.rect(self.screen,C.RED,[ux,uy-uw*0.5,uw,uw*0.5],2)   
                pygame.draw.rect(self.screen,C.RED,[ux,uy-uw*0.5,uw,uw*0.1],5)
                pygame.draw.rect(self.screen,C.WHITE,[ux,uy-uw*0.5,uw,uw*0.1],)  
                #self.draw_text("START & GOAL",ux+uw/2,uy-20-uw*0.5,C.BLACK,self.fnt_l) 
            side_w = uw * 0.3
            
            

            if game.mylocation == 0:
                pygame.draw.polygon(self.screen,col,[[ux,uy],[ux+uw,uy],[bx+bw,by],[bx,by]])   #道路の板を描く
                
                if int(game.p1.y+i)%10 <= 4:  #左右の黄色線を描画
                    pygame.draw.polygon(self.screen,C.YELLOW,[[ux,uy],[ux+uw*0.02,uy],[bx+bw*0.02,by],[bx,by]])      #左
                    pygame.draw.polygon(self.screen,C.YELLOW,[[ux+uw*0.98,uy],[ux+uw,uy],[bx+bw,by],[bx+bw*0.98,by]])   #右

                if int(game.p1.y+i)%20 <= 10:   #白線を描画
                    pygame.draw.polygon(self.screen,C.WHITE,[[ux+uw*0.24,uy],[ux+uw*0.26,uy],[bx+bw*0.26,by],[bx+bw*0.24,by]])  #左
                    pygame.draw.polygon(self.screen,C.WHITE,[[ux+uw*0.49,uy],[ux+uw*0.51,uy],[bx+bw*0.51,by],[bx+bw*0.49,by]])  #中央
                    pygame.draw.polygon(self.screen,C.WHITE,[[ux+uw*0.74,uy],[ux+uw*0.76,uy],[bx+bw*0.76,by],[bx+bw*0.74,by]])  #右

                pygame.draw.polygon(self.screen,C.BLACK,[[ux,uy],[bx,by],[bx-side_w,by],[ux-side_w,uy]])   #道路脇の板を描く(左)
                pygame.draw.polygon(self.screen,C.BLACK,[[ux+uw,uy],[ux+uw+side_w,uy],[bx+bw+side_w,by],[bx+bw,by]])   #道路脇の板を描く(右)

            if game.mylocation == 1:
                pygame.draw.polygon(self.screen,self.road_color(game,game.p1.y+i,col),[[ux,uy],[ux+uw,uy],[bx+bw,by],[bx,by]])   #道路の板を描く
            
            if game.mylocation == 2:
                pygame.draw.polygon(self.screen,self.road_color(game,game.p1.y+i,col),[[ux,uy],[ux+uw,uy],[bx+bw,by],[bx,by]])   #道路の板を描く
            
            """
            pygame.draw.polygon(self.screen,C.BLACK,[[ux,uy],[bx,by],[bx-side_w,by],[ux-side_w,uy]])   #道路脇の板を描く(左)
            pygame.draw.polygon(self.screen,C.BLACK,[[ux+uw,uy],[ux+uw+side_w,uy],[bx+bw+side_w,by],[bx+bw,by]])   #道路脇の板を描く(右)
"""
            
            scale = 1.5*C.BOARD_W[i]/C.BOARD_W[0]    #道路横の物体のスケールを計算
            obj_l = self.object_left[int(game.p1.y+i)%C.CMAX]   #道路左の物体
            obj_r = self.object_right[int(game.p1.y+i)%C.CMAX]  #道路右の物体
            obj_ul = self.object_uleft[int(game.p1.y+i)%C.CMAX]  #道路右の物体
            obj_ur = self.object_uright[int(game.p1.y+i)%C.CMAX]  #道路右の物体
            


            if game.mylocation == 0:  #Tokyo
                if obj_r == 1:  #ビル(右)
                    self.draw_obj(game.img_obj[obj_r],ux+uw*1.2,uy,scale)  
                if obj_l == 2: #ビル(左)
                    self.draw_obj(game.img_obj[obj_l],ux-uw*0.2,uy,scale)
                
            if game.mylocation == 1:  #Space
                for k in range(1,10):
                    if obj_r == k:
                        self.draw_obj(game.img_star[obj_r],ux+uw*1.2,uy,scale) 
                    if obj_l == k:
                        self.draw_obj(game.img_star[obj_l],ux-uw*0.2,uy,scale)
                    if obj_ul == k:
                        self.draw_obj(game.img_star[obj_ul],ux+uw*0.2,uy-uw*0.5,scale)
                    if obj_ur == k:
                        self.draw_obj(game.img_star[obj_ur],ux+uw*0.8,uy-uw*0.5,scale)
            
            if game.mylocation == 2:  #SD
                for k in range(1,29):
                    if obj_r == k:
                        self.draw_obj(game.img_sd[obj_r],ux+uw*1.2,uy,scale) 
                    if obj_l == k:
                        self.draw_obj(game.img_sd[obj_l],ux-uw*0.2,uy,scale)

            for c in range(1,C.CAR_NUM):                                      #繰り返しで
                if int(game.com.y[c])%C.CMAX == int(game.p1.y+i)%C.CMAX:          #その板にCOMカーがあるかどうか調べ
                    lr = int(4*(game.p1.x-game.com.x[c])/800)                 #プレイヤーから見たCOMカーの向きを計算し
                    if lr < -3:                                         #-3より小さいなら-3で
                        lr = -3
                    if lr > 3:                                          #3より大きいなら3で
                        lr = 3
                    self.draw_obj(game.img_car[(c%3)*7+3+lr],ux+game.com.x[c]*C.BOARD_W[i]/800,uy,0.05+C.BOARD_W[i]/C.BOARD_W[0])

            if i == game.p1.PLself: #PLAYERカー                                                                           #プレイヤーの車の位置なら
                self.draw_shadow(ux + game.p1.x * C.BOARD_W[i] / 800, uy, 200 * C.BOARD_W[i] / C.BOARD_W[0])  #車の影を描く
                self.draw_obj(game.img_car[3 + game.p1.lr + game.mycar*7], ux + game.p1.x * C.BOARD_W[i] / 800, uy, 0.05+ C.BOARD_W[i] / C.BOARD_W[0])  #プレイヤーの車を描く

            if game.mymode == 1:
                try:
                    self.draw_rival(game, self.screen, ux, uy)
                except:
                    pass
        
        #右側の部分の表示
        pygame.draw.rect(self.screen,C.WHITE,[800,0,300,600]) 
        self.make_map()
        self.map_pl(game, 900)
        if game.idx == 2:
            self.draw_text2("[F1] : Pause BGM",950,550,C.BLACK,self.fnt_ss)
            self.draw_text2("[F2] : Play BGM",950,580,C.BLACK,self.fnt_ss)

        
        self.draw_text(str(int(game.p1.spd)) + "km/h", 680, 30, C.RED, self.fnt_m)  #速度を表示
        if game.idx != 3:
            self.draw_text("lap {}/{}".format(game.laps + 1, C.LAPS), 100, 30, C.WHITE, self.fnt_m)  #周回数を表示    
        if game.idx == 3:
            self.draw_text("lap {}/{}".format(game.laps, C.LAPS), 100, 30, C.WHITE, self.fnt_m)  #補正した周回数を表示    
        self.draw_text("time " + game.p1.time_str(game.elapsed_time), 100, 80, C.GREEN, self.fnt_s)  #タイムを表示
        for i in range(game.laps):  #繰り返しで    
            self.draw_text(game.laptime[i], 80, 130 + 40 * i, C.YELLOW, self.fnt_s)  #ラップタイムを表示    

    def update_object(self, game):
        for i in range(C.CLEN):
            for j in range(C.BOARD):
                pos = j + C.BOARD*i  
                if game.mylocation == 0: #Tokyo
                    self.object_right[pos] = 0
                    self.object_left[pos] = 0
                    self.object_uleft[pos] = 0
                    self.object_uright[pos] = 0
                    if i%8 < 7:
                        if j%12 == 0 :
                            self.object_right[pos] = 1 #右のビル
                    if i%8 < 7:
                        if j%12 == 0 :
                            self.object_left[pos] = 2 #左のビル
                    """
                    else:
                        if j%20 == 0:
                            self.object_left[pos] = 3 #ヨット
                    if j%12 == 6:
                        self.object_left[pos] = 9 #海
                    """

                if game.mylocation == 1:  #Space
                    self.object_right[pos] = 0
                    self.object_left[pos] = 0
                    self.object_uleft[pos] = 0
                    self.object_uright[pos] = 0
                    if i%9 < 8:
                        if j == 0 :
                            self.object_right[pos] = self.star_sun1[i] 
                            self.object_uright[pos] = self.star_sun7[i] 
                        if j == 40 :
                            self.object_right[pos] = self.star_sun2[i]
                            self.object_uright[pos] = self.star_sun8[i]
                        if j == 80 :
                            self.object_right[pos] = self.star_sun3[i]
                            self.object_uright[pos] = self.star_sun9[i]
                        if j == 20 :
                            self.object_left[pos] = self.star_sun4[i] 
                            self.object_uleft[pos] = self.star_sun10[i] 
                        if j == 60  :
                            self.object_left[pos] = self.star_sun5[i]
                            self.object_uleft[pos] = self.star_sun11[i]
                        if j == 100 :
                            self.object_left[pos] = self.star_sun6[i]
                            self.object_uleft[pos] = self.star_sun12[i]
                
                if game.mylocation == 2:  #SD
                    self.object_right[pos] = 0
                    self.object_left[pos] = 0
                    self.object_uleft[pos] = 0
                    self.object_uright[pos] = 0
                    if i%28 < 27:
                        if j == 0 :
                            self.object_right[pos] = self.person_SD1[i] 
                        if j == 40 :
                            self.object_right[pos] = self.person_SD2[i]
                        if j == 80 :
                            self.object_right[pos] = self.person_SD3[i]
                        if j == 20 :
                            self.object_left[pos] = self.person_SD4[i] 
                        if j == 60  :
                            self.object_left[pos] = self.person_SD5[i]
                        if j == 100 :
                            self.object_left[pos] = self.person_SD6[i]
                                

    
    def make_map(self):
        pygame.draw.line(self.screen,C.BLACK,[850,500],[950,500],3)   #スタートラインの描画
        pygame.draw.line(self.screen,C.BLACK,[850,100],[950,100],3)     #ゴールラインの描画 
        txt_s = self.fnt_ss.render("Start",True,C.BLACK)           #Startの記述
        txt_g = self.fnt_ss.render("Goal",True,C.BLACK)            #Goalの記述
        self.screen.blit(txt_s,[810,490])
        self.screen.blit(txt_g,[810,90])
        for i in range(1,C.LAPS):    #ラップに対応したラインの描画
            pygame.draw.line(self.screen,C.BLACK,[850,100+int(i*400/C.LAPS)],[950,100+int(i*400/C.LAPS)],1)
            txt_lap = self.fnt_ss.render("{}/{}".format((C.LAPS-i),C.LAPS),True,C.BLACK)
            self.screen.blit(txt_lap,[810,100+int(i*400/C.LAPS)-10])


    def map_pl(self, game, x):
        pygame.draw.line(self.screen,C.BLACK,[x,500],[x,100],1)      #中心線の描画
        map_car_col = C.RED                 #車種によって円の色を変える
        if game.mycar == 0:
            map_car_col = C.RED
        if game.mycar == 1:
            map_car_col = C.GRAY
        if game.mycar == 2:
            map_car_col = C.YELLOW
        
        y = 100 + (C.CMAX * (C.LAPS - game.laps) - game.p1.y) * 400 / (C.CMAX * C.LAPS) #マップ上のy座標を計算
        pygame.draw.circle(self.screen, map_car_col, [x, int(y)], 8, 0) #マップ上に円を描画

        pl = ""           #プレイヤーがどちらなのかを入れる変数
        if game.p1 == game.p1: # ??どういう意味？
            pl = "1p"
        txt_pl = self.fnt_ss.render(pl,True,C.BLACK)
        self.screen.blit(txt_pl,[910,int(y)-10])

    def draw_rival(self, game, bg,ux,uy):  # 敵車の座標がlist出力 [400, 500] 確認してみて
            if game.player == 0:
                print(game.game.bothPos[1][0])
                self.draw_shadow(bg, ux + game.game.bothPos[1][0] * C.BOARD_W[i] / 800, uy, 200 * C.BOARD_W[i] / C.BOARD_W[0])  #車の影を描く
            elif game.player == 1:
                print(game.game.bothPos[0][0]) 


    def draw_obj(self, img, x, y, sc):                        #座標とスケールを受け取り、物体を描く関数
        img_rz = pygame.transform.rotozoom(img,0,sc)        #拡大縮小した画像を受け取る
        w = img_rz.get_width()                              #その画像の幅をwに代入
        h = img_rz.get_height()                             #その画像の高さをhに代入
        self.screen.blit(img_rz,[x-w/2,y-h])                         #画像を描く

    def draw_shadow(self, x, y, siz):  #車の影を表示する関数
        shadow = pygame.Surface([siz, siz / 4])  #描画面(サーフェース)を用意する
        shadow.fill(C.RED)  #その描画面を赤で埋めつくす
        shadow.set_colorkey(C.RED)  #Surfaceの透過色を指定
        shadow.set_alpha(128)  #Surfaceの透明度を指定
        pygame.draw.ellipse(shadow, C.BLACK, [0, 0, siz, siz / 4])  #描画面に黒で楕円を描く
        self.screen.blit(shadow, [x - siz / 2, y - siz / 4])  #楕円を描いた描画面をゲーム画面に転送
        

    def draw_text(self, txt, x, y, col, fnt):  #影付きの文字列を表示する関数
        sur = fnt.render(txt, True, C.BLACK)  #黒で文字列を描いたサーフェースを生成
        x -= sur.get_width() / 2  #センタリングするためx座標を計算
        y -= sur.get_height() / 2  #センタリングするためy座標を計算
        self.screen.blit(sur, [x + 2, y + 2])  #サーフェースを画面に転送
        sur = fnt.render(txt, True, col)  #指定色で文字列を描いたサーフェースを作成
        self.screen.blit(sur, [x, y])  #サーフェースを画面に転送

    def draw_text2(self, txt, x, y, col, fnt):
        sur = fnt.render(txt, True, col)
        self.screen.blit(sur,[x,y])

    def road_color(self,game,i,col):
        if game.mylocation == 1:
            if 0 <= i%21 and i%21 <= 2:
                col = C.RED
            if 3 <= i%21 and i%21 <= 5:
                col = C.ORANGE
            if 6 <= i%21 and i%21 <= 8:
                col = C.YELLOW
            if 9 <= i%21 and i%21 <= 11:
                col = C.LGREEN
            if 12 <= i%21 and i%21 <= 14:
                col = C.SKYBLUE
            if 15 <= i%21 and i%21 <= 17:
                col = C.BLUE
            if 18 <= i%21 and i%21 <= 20:
                col = C.PURPLE
        elif game.myoperation == 2:
            col = C.GRAY

        return col
