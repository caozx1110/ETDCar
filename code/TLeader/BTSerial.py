import serial
import serial.tools.list_ports
import threading
from PyQt5.QtCore import pyqtSignal
from time import sleep

# lock = threading.Lock()


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
        self.result = None

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            return None


class BTSerial:
    ReceiveData = []
    Reception = None
    TransData = None
    serial: serial.Serial

    def __init__(self, port, bps, time_out):
        self.Port = port            # port
        self.Bps = bps              # baud rate
        self.TimeOut = time_out    # time out
        self.IsConnected = False
        self.serial = serial.Serial(port, bps, timeout=time_out)
        if self.serial.is_open:
            print('Initialize the port successfully')
        # try:
        #     self.serial = serial.Serial(port, bps, timeout=time_out)
        #     if self.serial.is_open:
        #         print('Initialize the port successfully')
        # except Exception as e:
        #     print('Failed to initialize the port')

    def BasicInfo(self):
        print('Serial name: ', self.serial.name)
        print('Serial port: ', self.serial.port)
        print('Serial baudrate: ', self.serial.baudrate)
        print('Serial bytesize: ', self.serial.bytesize)
        print('Serial stopbits: ', self.serial.stopbits)
        print('serial parity: ', self.serial.parity)

    def OpenSerial(self):
        self.serial.open()

    def CloseSerial(self):
        self.serial.close()
        if not self.serial.is_open:
            print('The serial is closed')
        else:
            print('Fail to close')

    def Start(self):
        self.OpenSerial()
        if self.serial.is_open:
            print('Open successfully')
            return True
        else:
            print('Fail to open')
            return False

    def Receive(self, ReceiveFinished):
        while self.serial.is_open:
            try:
                if self.serial.in_waiting:
                    self.Reception = self.serial.read_all().hex()

                    print(self.Reception)
                    ReceiveFinished.emit(self.Reception)    # 发送信号
                    self.ReceiveData.append(self.Reception)
                    sleep(0.1)
            except Exception as e:
                pass

    def Transmit(self):
        # print(self.TransData)
        self.serial.write(self.TransData.encode('utf-8'))
        # sleep(0.2)


def PrintReception(reception):
    m = 0
    while True:
        if len(reception) == 0:
            sleep(1)
            continue
        else:
            if m == len(reception):
                sleep(1)
            else:
                m = len(reception)
                print(reception)
                sleep(1)


# if __name__ == '__main__':
#     port = 'COM6'
#     bps = 115200  # baud rate
#     time_out = 5
#     ser = BTSerial(port, bps, time_out)
#     data = None
#
#     t1 = MyThread(func=ser.Trans)
#     t2 = MyThread(func=ser.Receive)
#     t3 = MyThread(func=PrintReception, args=(ser.ReceiveData,))
#     t = [t1, t2, t3]
#     for thr in t:
#         thr.setDaemon(True)
#         thr.start()
#
#     while True:
#         print('main thread')
#         ser.TransData = input('')
#         sleep(0.5)

