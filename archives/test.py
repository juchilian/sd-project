import pygame

class Constants:
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
    CLEN = len(DATA_LR)  #左右のデータの要素数を代入した定数

class Game:
    def __init__(self):
        self.load_image()
    
    def load_image(self): #画像の読み込み
        self.img_bg = pygame.image.load("image_pr/bg.png").convert()  #背景(空と地面の絵)
    
    def run(self):
        pygame.init() #pygameモジュールの初期化                                                
        pygame.display.set_caption("Pygame Racer") #ウインドウに表示するタイトルを指定
        screen = pygame.display.set_mode((800,600)) #描画面を初期化
        print(self.img_bg)



if __name__ == '__main__':
    g = Game()
    g.run()
    