# coding=utf-8
"""
author: Cao Zhanxiang
project: ETDSerial
file: MainProgress.py
date: 2021/6/30
function: 多线程，蓝牙串口
"""

from BTSerial import BTSerial
from PyQt5.QtCore import QThread, pyqtSignal

BPS = 11520
TIMEOUT = 5

# 发送线程
class TransThread(QThread):
    # 结束信号
    TransFinished = pyqtSignal(str)
    BTS: BTSerial

    # 参数从构造函数传入
    def __init__(self, bts, data):
        super(TransThread, self).__init__()
        self.BTS = bts
        self.BTS.TransData = data

    def run(self):
        self.BTS.Transmit()
        # 参数传出，靠信号发出
        self.TransFinished.emit(self.BTS.TransData)

# 接收线程
class ReceiveThread(QThread):
    # 结束信号
    ReceiveFinished = pyqtSignal(str)
    BTS: BTSerial

    # 参数从构造函数传入
    def __init__(self, bts):
        super(ReceiveThread, self).__init__()
        self.BTS = bts

    def run(self):
        # self.SearchResult = Cds.Search(self.KeyWord)
        self.BTS.Receive(self.ReceiveFinished)


class MainProgress:
    TThread: TransThread
    RThread: ReceiveThread
    BTS: BTSerial

    def __init__(self):
        pass

    def SetBTS(self, com):
        self.BTS = BTSerial(com, BPS, TIMEOUT)

    # 发送data
    def Transmit(self, data):
        self.TThread = TransThread(self.BTS, data)
        self.TThread.start()

    # 接收信息
    def Receive(self):
        self.RThread = ReceiveThread(self.BTS)
        self.RThread.start()

    def CloseReceive(self):
        self.RThread.exit()


