from CAR_API import Car

car = Car()
import time

from evdev import InputDevice, categorize, ecodes, list_devices

import argparse
parser = argparse.ArgumentParser(description='Controller input for driving the car')
parser.add_argument('-d', '--device', default='/dev/input/event26', help='Specify the input device as /dev/input/eventi')
args = parser.parse_args()

if args.device:
    gamepad = InputDevice(args.device)
else:
    gamepad = InputDevice(list_devices()[0])

print("Using InputDevice", gamepad)

if False:
    while True:
        for event in gamepad.read_loop():
            print(event.code, event.type, event.value)

throttle = 0
steering = 0
old_accel = ""
old_steer = ""
while True:

    for event in gamepad.read_loop():
        #print(event.code, event.type, event.value)
        if event.type == 1:
            if event.value == 1:
                if event.code == 315: # start
                    car.start()
                    print("="*5, "start", "="*5)
                else:
                    car.stop()
                    print("="*5, "stop", "="*5)
        if event.type == 3: # analog
            if event.code == 9: # RT
                throttle = int(event.value * 100 / 2**16)
            elif event.code == 10: # LT
                throttle = -int(event.value * 100 / 2**16)

            if event.code == 0: # A1x
                steering = int((event.value-2**15) * 100 / 2**15)
            
        print(throttle, steering)
        sent, data = car.actuate(throttle, steering)
        print(data)
        retry_count = 0
        while not sent and retry_count<5:
            print("Not recieved")
            time.sleep(1)
            car.connect()
            car.test_connection()
            print("car.is_connected", car.is_connected)
            sent, data = car.actuate(throttle, steering)
            retry_count += 1
            print("car.is_connected2", car.is_connected)
            print("sent", sent)


