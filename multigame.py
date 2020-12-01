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
        self.started_time = 0

    def start_game(self):
        self.started_time = time.time()


    def reset_game(self):
        self.p1set = False
        self.p2set = False

    def bothGoal(self):
        return self.p1Goal and self.p2Goal
    
    def play(self, player, move):  #moveに座標が入ったobjectが入る
        self.bothPos[player] = [move.x, move.y]
    
    def connected(self):
        return self.ready
        


