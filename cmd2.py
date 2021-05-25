from CAR_API import Car

car = Car()
import time
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

import threading
from evdev import InputDevice, categorize, ecodes, list_devices


if False:
    gamepad = InputDevice(list_devices()[0])
    while True:
        for event in gamepad.read_loop():
            print(event.code, event.type, event.value)
            print( ( (event.value-2**15) ) )

def controller_loop(stdscr):
    global exit_sig
    gamepad = InputDevice(list_devices()[0])
    throttle = 0
    steering = 0
    old_accel = ""
    old_steer = ""
    last_update = time.time()
    while True:
        now = time.time()
        if exit_sig:
            break

        height, width = stdscr.getmaxyx()
        w = width - 20
        for event in gamepad.read_loop():
            #print(event.code, event.type, event.value)
            if event.type == 3: # analog
                if event.code == 9: # RT
                    throttle = int(event.value * 100 / 2**16)
                elif event.code == 10: # LT
                    throttle = -int(event.value * 100 / 2**16)

                if event.code == 0: # A1x
                    steering = int((event.value-2**15) * 100 / 2**15)
                

            car.actuate(throttle, steering)

        if now-last_update>1 or True:
            last_update = now
            accel = "#"*int(w*abs(throttle)/100) + " "*int(w*(100-abs(throttle))/100)

            s = (steering+100)/200.0
            steer = " "*int(s*w -2) + "<>" + " "*int(s*w -2)

            if accel!=old_accel:
                y,x = stdscr.getyx()
                if throttle<0:
                    stdscr.addstr(height-2, 0, "[break]   <<< " + str(accel))
                else:
                    stdscr.addstr(height-2, 0, "[accel]   <<< " + str(accel))
                stdscr.move(y, x)
                old_accel = accel
            if steer!= old_steer:
                y,x = stdscr.getyx()
                stdscr.addstr(height-3, 0, "[steer]   <<< " + str(steer))
                stdscr.move(y, x)
                old_steer = steer
            
            stdscr.refresh()
            pass

global car_data, car_reply
car_data = {}
car_reply = ""

global exit_sig
exit_sig = False
def data_loop(stdscr):
    old_reply = ""
    while True:
        height, width = stdscr.getmaxyx()

        car_data, car_reply = car.get_data()
        time.sleep(1)
        if old_reply != car_reply and car_reply!="":
            y,x = stdscr.getyx() 
            stdscr.addstr(3, 0, "[car]     <<< " + str(car_reply).replace('\n', '').replace('\r', '')[:width-10])
            stdscr.addstr(1, 0, "[data]    <<< " + str(car_data).replace('\n', '').replace('\r', '')[:width-10])
            stdscr.move(y, x)
            stdscr.refresh()
            old_reply = car_reply

        if exit_sig:
            break

def main(stdscr):
    global car_data, car_reply
    global exit_sig

    curses.beep()

    stdscr.clear()
    stdscr.refresh()
    
    controller_loop_thread = threading.Thread(target=controller_loop, args=(stdscr,) )
    controller_loop_thread.start()

    #data_loop_thread = threading.Thread(target=data_loop, args=(stdscr,) )
    #data_loop_thread.start()

    while True:
        
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        stdscr.refresh()
        
        #stdscr.addstr(1, 0, "[car]     <<< " + str(car_reply))
        stdscr.addstr(0, 0, "[console] >>> ")

        editwin = curses.newwin(1,30, 0,14)
        #rectangle(stdscr, 1,0, 1+5+1, 1+30+1)

        stdscr.refresh()

        box = Textbox(editwin)

        # Let the user edit until Ctrl-G is struck.
        message = box.edit()

        message = message.strip()
        #curses.flash()

        # Get resulting contents
        #message = box.gather()
        if "exit" in message:
            exit_sig = True
            #data_loop_thread.join()
            controller_loop_thread.join()
            exit()

        car.send_command(message)
        #stdscr.timeout(1000)
        #time.sleep(1)


    


wrapper(main)

exit()

