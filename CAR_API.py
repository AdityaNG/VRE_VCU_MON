import time
import serial

class Car:

    def __init__(self, port='/dev/rfcomm0', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.p_th = 0
        self.prev_cmd = ""
        self.data = {}
        self.chase = 0.5
        self.prev_actuate = ""
        self.is_connected = False
        self.last_sent_time = 0
        self.connect()
        self.test_connection()

    def connect(self):
        self.ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )
        self.ser.isOpen()

    def test_connection(self):
        self.data = {}
        self.get_data()
        self.is_connected = self.data == {}
        return self.is_connected
    
    def get_data(self):
        out = ""
        while self.ser.inWaiting() > 0:
            reading = self.ser.read(1)
            print(reading.decode('utf-8'), end='')
            out += reading.decode('utf-8')
        if out!= '':
            print()

        if out != '':
            self.data = {}
            for ele in out.split(","):
                if ':' in ele:
                    try:
                        key, val = ele.split(":")
                        key = key.strip()
                        val = float(val)
                        self.data[key] = val
                    except Exception as e:
                        print("Err ele : " + ele)
        return self.data, out.replace("\r", "").strip()

    def start(self):
        self.send_command("start;")

    def stop(self):
        self.send_command("stop;")

    def set_CURRENT_LIMIT(self, CURRENT_LIMIT):
        #if 'CURRENT_LIMIT' in self.data:
        self.send_command("CURRENT_LIMIT " + str(CURRENT_LIMIT).zfill(4) + ";")

    def actuate(self, th, st):
        th_n = int((th-self.p_th)*self.chase + self.p_th)
        self.p_th = th_n

        if th == 0 and False:
            self.p_th = 0
            th_n = 0

        th_str = ('-' if (th_n<0) else'+' ) + str(abs(th_n)).zfill(3)
        st_str = ('-' if (st<0) else'+' ) + str(abs(st)).zfill(3)
        cmd = "actuate " + th_str + " " + st_str + ";"
        if self.prev_actuate != cmd or True:
            self.prev_actuate = cmd
            return self.send_command(cmd)
    
    def send_command(self, inp):
        sent = False
        inp = ';' + inp
        now = time.time()
        if not self.is_connected:
            return False, ({}, 'DISCONNECTED')
        #if self.prev_cmd != inp or now - self.last_sent_time > 0.05:
        if self.prev_cmd != inp:
            try:
                print(">>>", inp)
                self.last_sent_time = now
                self.ser.write(str(inp + '\r').encode('utf-8'))    
                self.prev_cmd = inp
                sent = True
                self.is_connected = True
            except Exception as e:
                print("Connection Error : " + str(e))
                sent = False
                self.is_connected = False
        else:
            sent = True
        return sent, self.get_data()

