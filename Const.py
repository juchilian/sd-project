from math import sin,radians
# Constants
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

#道路の板の基本形状を計算
CAR_NUM = 30
BOARD = 120
CMAX = BOARD * CLEN
BOARD_W = [0]* BOARD                            #板の幅を代入するリスト
BOARD_H = [0]* BOARD                            #板の高さを代入する
BOARD_UP = [0]* BOARD                           #板の起伏用の値を代入するりすと
for i in range(BOARD):                         #繰り返しで
    BOARD_W[i] = 10 + (BOARD-i)*(BOARD-i)/12    #幅を計算
    BOARD_H[i] = 3.4*(BOARD-i)/BOARD            #高さを計算
    BOARD_UP[i] = 2*sin(radians(i*1.5))         #起伏の値を三角関数で計算

