# coding=utf-8
"""
author: Cao Zhanxiang
project: ETDSerial
file: example.py
date: 2021/7/1
function: 
"""

from BTSerial import *

def print_loop(item):
    while True:
        if item is not None:
            print(item)
        sleep(2)


if __name__ == '__main__':
    port = 'COM6'
    bps = 115200
    time_out = 5
    ser = BTSerial(port, bps, time_out=time_out)

    t1 = MyThread(func=ser.Receive)
    t2 = MyThread(func=print, args=(ser.Reception, ))
    t = [t1, t2]
    for thr in t:
        thr.setDaemon(True)
        thr.start()

    for thr in t:
        thr.join()

    while True:
        if ser.Reception is not None:
            print(ser.Reception)
        sleep(2)
