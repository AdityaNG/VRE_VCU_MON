# Bluetooth Serial Controller

<img src="imgs/console.png">

<img src="imgs/graph.png">

A robust bluetooth serial controller to display accelerometer data, CAN data, SD card logs, live graphs and remote shutdown the car

## TODO

1. UI - Console
2. UI - Graphing
3. Console API
4. Graphing API

## Data format

The commands are issued with options and terminated with a semi-colon. The output is also sent in a similar format.

## Setup and Dependencies

Install the following

```bash
sudo apt-get install bluetooth libbluetooth-dev
python3 -m pip install -r requirements.txt
```

To scan for devices :
```bash
hcitool scan
Scanning ...
	AC:67:B2:36:23:0E	VRE_VCU
```

To bind :
```bash
# bind 0 refers to device number 0 (rfcomm0) and 1 is the channel.
sudo rfcomm bind 0 AC:67:B2:36:23:0E 1
```
Now, pySerial at /dev/rfcomm0 with 115200 baud rate will work.

## Refrences

https://askubuntu.com/questions/114171/why-is-dev-rfcomm0-giving-pyserial-problems

https://www.programmersought.com/article/10551229226/

https://unix.stackexchange.com/questions/92255/how-do-i-connect-and-send-data-to-a-bluetooth-serial-port-on-linux
