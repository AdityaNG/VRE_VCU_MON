import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
from CAR_API import Car

car = Car()


import pygame
pygame.init()
pygame.display.set_mode()

global win
throttle=0
steering=0
MAX_TH = 255 * 0.5
MAX_ST = 255
creep_mode = 0
width = 500
win = pygame.display.set_mode((width, width))
data = {}

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

MAX_CURRENT_L = 0
MAX_CURRENT_R = 0
CURRENT_LIMIT = 2000

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

def get_data(key):
    if key not in data:
        return 0.0
    return data[key]

def draw_win():
    global win, MAX_CURRENT_L, MAX_CURRENT_R
    
    cur_l = get_data('CURRENT_DRAW_L')

    if cur_l > MAX_CURRENT_L:
        MAX_CURRENT_L = cur_l
        print("MAX_CURRENT_L : ", MAX_CURRENT_L)
    
    cur_r = get_data('CURRENT_DRAW_R')

    if cur_r > MAX_CURRENT_R:
        MAX_CURRENT_R = cur_r
        print("MAX_CURRENT_R : ", MAX_CURRENT_R)

    font = pygame.font.Font('freesansbold.ttf', 12)

    current_l_text = font.render('CURRENT_DRAW_L : ' + str(int(cur_l)), True, green, blue)
    current_r_text = font.render('CURRENT_DRAW_R : ' + str(int(cur_r)), True, green, blue)
    
    current_l_textRect = current_l_text.get_rect()
    current_r_textRect = current_r_text.get_rect()
    current_l_textRect.center = (width//2, 70)
    current_r_textRect.center = (width//2, 170)

    win.fill( black )
    win.blit(current_l_text, current_l_textRect)
    win.blit(current_r_text, current_r_textRect)
    
    min_cutoff = 1300
    cur_l_w = cur_l
    if cur_l > min_cutoff:
        cur_l_w -= min_cutoff
    
    cur_r_w = cur_r
    if cur_r > min_cutoff:
        cur_r_w -= min_cutoff

    pygame.draw.rect(win, ( int(255 * (cur_l_w)/(4095-min_cutoff)), int(255 * (1 - cur_l_w/(4095-min_cutoff)) ) , 0) , pygame.Rect(0, 0, int(width * cur_l_w/(4095-min_cutoff)), 50))
    pygame.draw.rect(win, ( int(255 * (cur_r_w)/(4095-min_cutoff)), int(255 * (1 - cur_r_w/(4095-min_cutoff)) ) , 0) , pygame.Rect(0, 100, int(width * cur_r_w/(4095-min_cutoff)), 50))
    pygame.display.flip()
    
    pygame.display.update()


print(joysticks)

while 1 :
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            ser.close()
            pygame.quit() #sys.exit() if sys is imported
            exit()
        if event.type == pygame.JOYAXISMOTION:
            j = event.joy, event.axis, event.value
            if event.axis == 5: # Break
                throttle = int((event.value+1) /2 * -MAX_TH)
                creep_mode = 0
            elif event.axis == 4: # Throttle
                throttle = int((event.value+1) /2 * MAX_TH)
                creep_mode = 0

            if event.axis == 0: # Steer
                steering = int(event.value * MAX_ST)

        if event.type == pygame.JOYBUTTONUP:
            if event.button == 7 or event.button == 6: # RB or LB
                #creep_mode = 0
                pass
            elif event.button == 3: # x
                car.regen = False
        if event.type == pygame.JOYBUTTONDOWN:
            j = event.joy, event.button
            print(j)
            if event.button == 11: # Start
                car.start()
                print("=========start==========")
            elif event.button == 1: # b
                CURRENT_LIMIT = (CURRENT_LIMIT + 500) % 4095
                print("CURRENT_LIMIT: " + str(CURRENT_LIMIT))
                car.set_CURRENT_LIMIT(CURRENT_LIMIT)
            elif event.button == 4: # y
                creep_mode = 0
                throttle = 0
            elif event.button == 7: # RB
                creep_mode = 1
            elif event.button == 6: # LB
                creep_mode = -1
            elif event.button == 3: # x
                car.regen = True

            elif event.button == 0: # A
                throttle = 0
                creep_mode = 0
            else:
                car.stop()
                print("=========stop==========")

        if creep_mode!=0:
            throttle = creep_mode * int(15 + 10*abs(steering)/100.0)


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                throttle = MAX_TH
            elif event.key == pygame.K_s:
                throttle = -MAX_TH

            if event.key == pygame.K_a:
                steering = MAX_ST
            elif event.key == pygame.K_d:
                steering = -MAX_ST
            
            if event.key == pygame.K_q:
                exit()

            if event.key == pygame.K_x:
                creep_mode = -1
            elif event.key == pygame.K_v:
                creep_mode = 1
            if event.key == pygame.K_c:
                creep_mode = 0
                throttle = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                throttle = 0
            elif event.key == pygame.K_s:
                throttle = 0

            if event.key == pygame.K_a:
                steering = 0
            elif event.key == pygame.K_d:
                steering = 0
            
            if event.key == pygame.K_o:
                car.start()
            elif event.key == pygame.K_p:
                car.stop()
            
            if event.key == pygame.K_x or event.key == pygame.K_v:
                creep_mode = 0
                throttle = 0
        
    else:
        car.actuate(throttle, steering)
    
    pygame.time.delay(10)
    data = car.get_data()
    draw_win()
    # {'ax': 1788.0, ' ay': 512.0, ' az': -15148.0, ' gx': 263.0, ' gy': -212.0, ' gz': 183.0, ' CURRENT_DRAW_L': 1616.0, ' CURRENT_DRAW_R': 1918.0, ' throttle_val': 1.0, ' steering_val': 0.0, ' RTC_TIME': 0.0}


