import time
import serial
import matplotlib.pyplot as plt

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/rfcomm0',
    baudrate=115200,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()

global history, fig
history = dict()
fig = False

def render_data(data, keys=['ax', 'ay', 'az', 'gx', 'gy', 'gz']):
    global history, fig, axs
    if not fig:
        fig, axs = plt.subplots(len(keys))
        fig.suptitle('Vertically stacked subplots')
    for k in keys:
        if k not in data:
            print("Empty")
            return
    for k in keys:
        #print(k + ":" + data[k], end=", ")
        history.setdefault(k, [])
        history[k].append(data[k])
        if len(history[k])>50:
            history[k].pop(0)
    print()
    for i,k in enumerate(keys):
        print(k, history[k])
        axs[i].plot(history[k])
        axs[i].set_title(k)
        #plt.plot(1)  
    #fig.draw()
    plt.pause(1)
    plt.show(block=False)

    pass

data = dict()
while 1 :
    #print(data)
    render_data(data)
    out = ''
    while ser.inWaiting() > 0:
        out += ser.read(1).decode('utf-8')

    if out != '' and "," in out and ":" in out:
        for ele in out.split(","):
            if ":" in ele:
                k, v = list(map(lambda x:x.strip(), ele.split(":")))
                data[k] = v
                #print(k, v)
