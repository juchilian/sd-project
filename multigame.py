import pygame
import sys
from math import sin,radians
import random
from pygame.locals import *  #pygame.定数の記述の省略
import Const as C
from player import Player
from computer import Computer
from network import Network
import time


class MultiGame:
    def __init__(self, id):
        self.p1Goal = False
        self.p2Goal = False
        self.ready = False
        self.id = id
        self.bothPos = [[300, 0], [500, 0]]        
        self.wins = [0, 0]

    def reset_game():
        self.p1set = False
        self.p2set = False

    def bothGoal(self):
        return self.p1Goal and self.p2Goal
    
    def play(self, player, move):  #moveに座標が入ったobjectが入る
        self.bothPos[player] = [move.x, move.y]
        # if player == 0:
        #     self.p1Goal = True
        # else:
        #     self.p2Goal = True
    
    def connected(self):
        return self.ready
        
    




