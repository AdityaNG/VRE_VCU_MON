import time
import serial

class Car:

    def __init__(self, port='/dev/rfcomm0', baudrate=115200):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )

        self.ser.isOpen()
        self.p_th = 0
        self.prev_cmd = ""
        self.data = {}
        self.chase = 0.5
    
    def get_data(self):
        out = ""
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1).decode('utf-8')

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
        self.send_command(cmd)
    
    def send_command(self, inp):
        sent = False
        if self.prev_cmd != inp:
            try:
                self.ser.write(str(inp + '\r').encode('utf-8'))    
                self.prev_cmd = inp
                sent = True
            except Exception as e:
                print("Connection Error : " + str(e))
                sent = False
        return sent

