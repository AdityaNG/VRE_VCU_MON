from CAR_API import Car

car = Car()
import time

from evdev import InputDevice, categorize, ecodes, list_devices

import argparse
parser = argparse.ArgumentParser(description='Controller input for driving the car')
parser.add_argument('-d', '--device', help='Specify the input device as /dev/input/eventi')
args = parser.parse_args()

if False:
    if args.device:
        gamepad = InputDevice(args.device)
    else:
        gamepad = InputDevice(list_devices()[0])
    while True:
        for event in gamepad.read_loop():
            print(event.code, event.type, event.value)
            print( ( (event.value-2**15) ) )

gamepad = InputDevice(list_devices()[0])
throttle = 0
steering = 0
old_accel = ""
old_steer = ""
while True:

    for event in gamepad.read_loop():
        #print(event.code, event.type, event.value)
        if event.type == 1:
            if event.code == 315: # start
                car.start()
                print("="*5, "start", "="*5)
            else:
                car.stop()
        if event.type == 3: # analog
            if event.code == 9: # RT
                throttle = int(event.value * 100 / 2**16)
            elif event.code == 10: # LT
                throttle = -int(event.value * 100 / 2**16)

            if event.code == 0: # A1x
                steering = int((event.value-2**15) * 100 / 2**15)
            
        print(throttle, steering)
        car.actuate(throttle, steering)


