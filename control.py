import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/rfcomm0',
    baudrate=115200,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()

import pygame
pygame.init()
pygame.display.set_mode()

print('Enter your commands below.\r\nInsert "exit" to leave the application.')

global p_th
p_th = 0
chase = 0.5
def gen_cmd(th, st):
    global p_th
    th_n = int((th-p_th)*chase + p_th)
    p_th = th_n

    if th == 0 and False:
        p_th = 0
        th_n = 0

    th_str = ('-' if (th_n<0) else'+' ) + str(abs(th_n)).zfill(3)
    st_str = ('-' if (st<0) else'+' ) + str(abs(st)).zfill(3)
    return "actuate " + th_str + " " + st_str + ";"

def send_command(inp):
    sent = False
    while not sent:
        try:
            ser.write(str(inp + '\r').encode('utf-8'))
            sent = True
        except Exception as e:
            print("Connection Error : " + str(e))
            time.sleep(1)

prev_cmd = ''
inp=1
throttle=0
steering=0
MAX_TH = 60
MAX_ST = 100
creep_mode = 0
width = 500
win = pygame.display.set_mode((width, width))

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

print(joysticks)

while 1 :
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            ser.close()
            pygame.quit() #sys.exit() if sys is imported
            exit()
        if event.type == pygame.JOYAXISMOTION:
            j = event.joy, event.axis, event.value
            print(j)
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
        if event.type == pygame.JOYBUTTONDOWN:
            j = event.joy, event.button
            print(j)
            if event.button == 11: # Start
                inp = "start;"
                send_command(inp)
                print("=========start==========")
            elif event.button == 4: # y
                creep_mode = 0
            elif event.button == 7: # RB
                creep_mode = 1
            elif event.button == 6: # LB
                creep_mode = -1
            elif event.button == 0: # A
                throttle = 0
                creep_mode = 0
            else:
                inp = "stop;"
                send_command(inp)
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
                inp = "exit"
                break
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                throttle = 0
            elif event.key == pygame.K_s:
                throttle = 0

            if event.key == pygame.K_a:
                steering = 0
            elif event.key == pygame.K_d:
                steering = 0
        
        # get keyboard inp
        #inp = input(">> ")
            # Python 3 users
            # inp = inp(">> ")
    if inp == 'exit':
        ser.close()
        exit()
    else:
        if inp!="start;" and event!="stop;":
            inp = gen_cmd(throttle, steering)
            #inp = gen_cmd(throttle, 100)
        
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        if inp != prev_cmd:
            send_command(inp)
            #ser.write(str(inp + '\r').encode('utf-8'))
            prev_cmd = inp
            print(">> " + inp)
        #out = ''
        # let's wait one second before reading output (let's give device time to answer)
        #time.sleep(1)
        #while ser.inWaiting() > 0:
        #    out += ser.read(1).decode('utf-8')

        #if out != '':
        #    print(">>" + out)
    #time.sleep(0.1)
    pygame.time.delay(200)
    if inp=='start;' or event=='stop;':
        inp = 1


