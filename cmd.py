from CAR_API import Car

car = Car()
import time
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

import threading

global car_data, car_reply
car_data = {}
car_reply = ""

global exit_sig
exit_sig = False
def data_loop(stdscr):
    old_reply = ""
    while True:
        car_data, car_reply = car.get_data()
        time.sleep(0.1)
        if old_reply != car_reply:
            y,x = stdscr.getyx() 
            stdscr.addstr(1, 0, "[car]     <<< " + str(car_reply))
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
    
    data_loop_thread = threading.Thread(target=data_loop, args=(stdscr,) )
    data_loop_thread.start()

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
            data_loop_thread.join()
            exit()

        car.send_command(message)
        #stdscr.timeout(1000)
        #time.sleep(0.5)


    


wrapper(main)

exit()

