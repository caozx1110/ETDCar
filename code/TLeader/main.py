# coding=utf-8
"""
author: Cao Zhanxiang
project: ETDSerial
file: main.py
date: 2021/6/29
function: 
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QFileDialog
from MainWindowUI import *
from MainProgress import MainProgress
from time import sleep

class MainWindow(QtWidgets.QWidget, Ui_TI_RSLK):
    Mp = MainProgress()
    Order = []
    OrderIdx = -1   # 当前读到的指令idx

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("TLeader.ico"))
        QtWidgets.QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.BeautifyUI()
        Map = QtGui.QPixmap('Map.bmp').scaled(600, 450)
        self.lbl_Map.setPixmap(Map)

    def cbx_ComSelect_currentTextChanged(self):
        pass

    # 连接蓝牙
    def pbtn_Connect_clicked(self):
        # 未连接，点击连接
        if self.pbtn_Connect.text() == 'Connect':
            try:
                self.Mp.SetBTS(self.cbx_ComSelect.currentText().lower())
                # 连接成功
                if self.Mp.BTS.serial.is_open:
                    # 接收打开
                    self.Mp.Receive()
                    # 连接槽函数
                    self.Mp.RThread.ReceiveFinished.connect(self.slot_ReceiveFinished)
                    self.lbl_Info.setText("Succeed to connect.")    # info
                    self.pbtn_Connect.setText('Disconnect')
                    self.pbtn_Connect.setStyleSheet("background-color:rgb(193, 210, 240);font-family:微软雅黑;font-size:16px")     #浅蓝色
                # self.Mp.BTS.OpenSerial()
            except Exception as e:
                self.lbl_Info.setText("Fail to connect.")
        # 已连接，点击断开
        else:
            try:
                self.Mp.BTS.CloseSerial()
                # info
                if not self.Mp.BTS.serial.is_open:
                    # self.Mp.CloseReceive()
                    self.lbl_Info.setText("Succeed to disconnect.")
                    self.lbl_Angle.setText("Angle: ")
                    self.lbl_State.setText("State: ")
                    self.lbl_CurrentOrder.setText("Order: ")
                    self.pbtn_Connect.setText('Connect')
                    self.pbtn_Connect.setStyleSheet("background-color:rgb(225, 225, 225);font-family:微软雅黑;font-size:16px")  # 原来的颜色
            except Exception as e:
                self.lbl_Info.setText("Fail to disconnect.")

    # 发送
    def pbtn_Send_clicked(self):
        Msg = self.ledt_SendMsg.text()
        self.SendMsg(Msg)

    def SendMsg(self, Msg):
        if self.IsSendMsgValid(Msg):
            Data = Msg.split('+')
            # 简单格式: <Direction>
            if len(Data) == 1:
                try:
                    self.Mp.Transmit(Data[0])
                    self.lbl_Info.setText("Succeed to send.")
                    self.lbl_State.setText("State: Run")
                except Exception as e:
                    self.lbl_Info.setText("Fail to send.")
            # 复杂格式: <Angle>+<Speed>+<Distance>
            elif len(Data) == 3:
                try:
                    AngleH, AngleL = self.AngleToBit8(float(Data[0]))   # 高位，低位
                    self.Mp.Transmit(chr(AngleH))
                    sleep(0.1)
                    self.Mp.Transmit(chr(AngleL))
                    sleep(0.1)
                    self.Mp.Transmit(Data[1])
                    sleep(0.1)
                    self.Mp.Transmit(chr(int(Data[2])))
                    sleep(0.1)
                    self.lbl_State.setText("State: Run")
                    self.lbl_Info.setText("Succeed to send.")
                except Exception as e:
                    self.lbl_Info.setText("Fail to send.")
        else:
            self.lbl_Info.setText("The format is incorrect.")
            self.ledt_SendMsg.clear()

    def ledt__SendMsg_returnPressed(self):
        self.pbtn_Send_clicked()

    # 导入文件
    def pbtn_Import_clicked(self):
        Map = QtGui.QPixmap("Map1.jpg").scaled(600, 450)
        self.lbl_Map.setPixmap(Map)
        FileName, FileType = QFileDialog.getOpenFileName(self, "选取文件", "", "Text Files (*.txt);;All Files (*)")
        if FileName != "":
            with open(FileName) as f:
                self.Order = f.read().splitlines()
                # print(Order)
                # 发出第一条指令
                if len(self.Order):
                    self.OrderIdx = 0
                    self.SendMsg(self.Order[self.OrderIdx])
                    self.lbl_CurrentOrder.setText(self.Order[self.OrderIdx])
                    self.OrderIdx = self.OrderIdx + 1
                    # 其余指令均在接收到小车返回的指令执行结束后执行
                else:
                    self.lbl_Info.setText("The file is empty.")

    # 接收到信息, 待完善
    def slot_ReceiveFinished(self, Data):
        # 如果是四位16进制数，认为是角度的高低位
        if len(Data) == 4:
            AngleH = int(Data[0:2], 16)
            AngleL = int(Data[2:4], 16)
            Angle = (AngleH * 256 + AngleL) * 180 / 32768
            Angle = format(Angle, '.1f')
            self.lbl_Angle.setText("Angle: " + str(Angle) + "°")
        elif len(Data) == 2:
            State = chr(int(Data, 16))
            # One order ends:
            # To supply code
            # 指令执行结束
            if State == 'E':
                try:
                    self.lbl_State.setText("State: Stop")
                    if self.OrderIdx < len(self.Order):
                        self.SendMsg(self.Order[self.OrderIdx])
                        self.lbl_CurrentOrder.setText("Order: " + self.Order[self.OrderIdx])
                        self.OrderIdx = self.OrderIdx + 1
                    else:
                        self.lbl_Info.setText("Order all done.")
                except Exception as e:
                    self.lbl_Info.setText("No next order.")
            # 遇到障碍，更改路径
            elif State == 'C':
                with open("Map2.txt") as f:
                    self.Order = f.read().splitlines()
                    Map = QtGui.QPixmap("Map2.jpg").scaled(600, 450)
                    self.lbl_Map.setPixmap(Map)
                    if len(self.Order):
                        self.OrderIdx = 0
                        self.SendMsg(self.Order[self.OrderIdx])
                        self.lbl_CurrentOrder.setText(self.Order[self.OrderIdx])
                        self.OrderIdx = self.OrderIdx + 1
        else:
            self.lbl_Info.setText("Receive error.")

    # 简单格式: <Direction>, 复杂格式: <Angle>+<Speed>+<Distance>
    def IsSendMsgValid(self, Msg) -> bool:
        Data = Msg.split('+')
        # 简单指令
        if len(Data) == 1:
            if Data[0] in ['F', 'B', 'L', 'R', 'S']:
                return True
            else:
                return False
        # 复杂指令
        elif len(Data) == 3:
            # Angle, float
            try:
                Angle = float(Data[0])
            except Exception as e:
                return False
            # SpeedLevel
            if Data[1] not in ['h', 'm', 'l']:
                return False
            # Distance
            try:
                Distance = int(Data[2])
                if 0 <= Distance <= 255:
                    return True
                else:
                    return False
            except Exception as e:
                return False
        else:
            return False

    # float 转为两个8位int
    def AngleToBit8(self, Angle):
        AngleHL = int(Angle * 32768 / 180)
        AngleH = AngleHL // 256  # 高位
        AngleL = AngleHL % 256  # 低位

        return AngleH, AngleL

    def BeautifyUI(self):
        self.setWindowOpacity(0.9)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # self.setStyleSheet('''
        #     QWidget#TI_RSLK{
        #     color:#232C51;
        #     background:white;
        #     border-top:1px solid darkGray;
        #     border-bottom:1px solid darkGray;
        #     border-right:1px solid darkGray;
        #     border-top-right-radius:10px;
        #     border-bottom-right-radius:10px;
        #     }
        # ''')
        pass

    # def pbtn_Min_clicked(self):
    #     self.setWindowState(Qt.WindowMinimized)
    #
    # def pbtn_Max_clicked(self):
    #     if self.windowState() == Qt.WindowNoState:
    #         self.setWindowState(Qt.WindowMaximized)
    #     else:
    #         self.setWindowState(Qt.WindowNoState)
    #
    # def pbtn_Close_clicked(self):
    #     self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
