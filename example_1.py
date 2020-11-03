import sys
#import random
import math
import pygame

BLACK = (  0,  0,  0)
SILBER = (192,192,192)

SIZE = (1200,700)

car_x = 400
car_y = 200
img_car = pygame.image.load("img/car_3.png")
img_car_now = img_car
car_w = img_car.get_width()
car_h = img_car.get_height()
car_center = (car_w / 2 ,car_h / 2)
reposition_x = 0
reposition_y = 0

arg = 0 #度
arg_rotate = 10

img_rotate = img_car
car_rotate_w = img_rotate.get_width()
car_rotate_h = img_rotate.get_height()
car_speed = 20

def move_car():
    global car_x,car_y,reposition_x,reposition_y,img_car_now
    global car_rotate_w,car_rotate_h,arg
    key = pygame.key.get_pressed()
    arg_rad = arg * math.pi / 180 #ラジアン

    if key[pygame.K_UP] == 1:
        car_x = car_x - car_speed * math.sin(arg_rad)
        car_y = car_y - car_speed * math.cos(arg_rad)
    if key[pygame.K_DOWN] == 1:
        car_x = car_x + car_speed * math.sin(arg_rad)
        car_y = car_y + car_speed * math.cos(arg_rad)
    if key[pygame.K_RIGHT] == 1:
        arg = arg - arg_rotate
        img_rotate = pygame.transform.rotozoom(img_car,arg,1)
        car_rotate_w = img_rotate.get_width()
        car_rotate_h = img_rotate.get_height()
        reposition_x = (car_rotate_w - car_w) / 2
        reposition_y = (car_rotate_h - car_h) / 2
        img_car_now = img_rotate

    if key[pygame.K_LEFT] == 1:
        arg = arg + arg_rotate
        img_rotate = pygame.transform.rotozoom(img_car,arg,1)
        car_rotate_w = img_rotate.get_width()
        car_rotate_h = img_rotate.get_height()
        reposition_x = (car_rotate_w - car_w) / 2
        reposition_y = (car_rotate_h - car_h) / 2
        img_car_now = img_rotate
    if arg == -360 or arg == 360 :
        arg = 0
        
        

def main():
    pygame.init()
    pygame.display.set_caption("車の表示")
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(SILBER)
        move_car()    
        screen.blit(img_car_now,[car_x,car_y],
                    ((car_rotate_w/2)-40,(car_rotate_h/2)-40,
                     80,80))
        
        pygame.display.update()
        clock.tick(20)

if __name__ == '__main__':
    main()
