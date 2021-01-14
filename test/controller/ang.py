import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop
from datetime import datetime


class ang(QAxWidget):



    def __init__(self):
        # print("kiwoom() class start")
        print("hello")
        super().__init__()
        self.login_event_loop = None
        self.calculator_event_loop = QEventLoop()
        self.all_stock_dict = {}

        self.account_stock_dict = {}

        self.get_ocx_instance()
        self.event_slots()
        self.signal_login_commConnect()


        min_data = []

    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)
        self.OnReceiveMsg.connect(self.msg_slot)

    def signal_login_commConnect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def login_slot(self, err_code):
        self.login_event_loop.exit()

    def stop_screen_cancel(self, sScrNo=None):
        self.dynamicCall("DisconnectRealData(QString)", sScrNo)

    def msg_slot(self, sScrNo, sRQName, sTrCode, msg):
        pass

    def get_min_data(self, code, tick, sPrevNext):
        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
        self.dynamicCall("SetInputValue(QString, QString)", "틱범위", tick)
        self.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")
        self.dynamicCall("CommRqData(QString,QString,int,QString)", "주식분봉차트조회", "opt10080", sPrevNext, "2000")
        self.calculator_event_loop.exec_()
        return self. min_data

    def tr_data_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == "주식분봉차트조회":
            code = self.dynamicCall("GetCommData(QString, QString, int , QString)", sTrCode, sRQName, 0, "종목코드")
            data = self. dynamicCall("GetCommDataEx(QString, QString)", sTrCode, sRQName)
            self.min_data = data
            self.calculator_event_loop.exit()
