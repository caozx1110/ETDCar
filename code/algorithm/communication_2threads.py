import serial
import serial.tools.list_ports
import threading
from time import sleep

lock = threading.Lock()


class my_thread(threading.Thread):
    def __init__(self, func, args=()):
        super(my_thread, self).__init__()
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


class blue_tooth_port:
    def __init__(self, port, bps, time_out):
        self.port = port  # port
        self.bps = bps  # baud rate
        self.time_out = time_out  # time out
        self.is_connected = False
        try:
            self.serial = serial.Serial(port, bps, timeout=time_out)
            if self.serial.is_open:
                print('Initialize the port successfully')
        except Exception as e:
            print('Failed to initialize the port')

    def basic_info(self):
        print('Serial name: ', self.serial.name)
        print('Serial port: ', self.serial.port)
        print('Serial baudrate: ', self.serial.baudrate)
        print('Serial bytesize: ', self.serial.bytesize)
        print('Serial stopbits: ', self.serial.stopbits)
        print('serial parity: ', self.serial.parity)

    def close_serial(self):
        self.serial.close()
        if not self.serial.is_open:
            print('The serial is closed')
        else:
            print('Fail to close')

    def receiver(self):
        global receive_data
        while True:
            if self.serial.in_waiting:
                reception = self.serial.read_all()
                receive_data.append(reception.hex())
            sleep(0.2)

    def transmitter(self):
        global data
        while True:
            if data is None:
                sleep(0.2)
                continue
            else:
                self.serial.write(data.encode('utf-8'))
                data = None
                sleep(0.2)


def print_reception(reception):
    m = 0
    while True:
        if len(reception) == 0:
            sleep(2)
            continue
        else:
            if m != len(reception):
                print(reception)
                m = len(reception)
                sleep(2)
            else:
                sleep(2)
                continue


def transfer_16(word_16):
    return int(word_16, base=16)


def transfer_32(word_32):
    dec_data = int(word_32, base=16)
    if dec_data > 2 ** 31 - 1:
        dec_data = - (2 ** 32 - dec_data)
    return dec_data


if __name__ == '__main__':
    port = 'COM8'  # port number
    bps = 115200  # baud rate
    time_out = 5
    ser = blue_tooth_port(port, bps, time_out)
    receive_data = []
    data = None

    t1 = my_thread(func=ser.transmitter)
    t2 = my_thread(func=ser.receiver)
    t3 = my_thread(func=print_reception, args=(receive_data, ))
    t = [t1, t2, t3]
    for thr in t:
        thr.setDaemon(True)
        thr.start()

    while True:
        data = input('')
        sleep(1)

