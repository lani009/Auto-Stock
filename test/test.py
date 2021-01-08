# from PyQt5.QAxContainer import QAxWidget
# from PyQt5.QtCore import QEventLoop
# from PyQt5.QtWidgets import QApplication
# import sys


# class Test(QAxWidget):
#     def __init__(self):
#         super().__init__()

#         self.setControl("KHOPENAPI.KHOpenAPICtrl.1")  # 레지스트리에 저장된 api 모듈 불러오기
#         self.login_event_loop = QEventLoop()
#         self.slot()
#         self.signal_login_commConnect()

#         self.global_event_loop = QEventLoop()

#         self.print_bunbong("104040")
#         self.global_event_loop.exec_()

#         self.print_bunbong("009830")
#         self.global_event_loop.exec_()

#         self.print_bunbong("009830")
#         self.global_event_loop.exec_()

#         self.print_bunbong("009830")
#         self.global_event_loop.exec_()

#         self.print_bunbong("009830")
#         self.global_event_loop.exec_()

#         self.print_bunbong("009830")
#         self.global_event_loop.exec_()

#         self.print_bunbong("009830")
#         self.global_event_loop.exec_()

#         self.print_bunbong("009830")
#         self.global_event_loop.exec_()

#         self.print_bunbong("009830")
#         self.global_event_loop.exec_()

#         self.print_bunbong("009830")
#         self.global_event_loop.exec_()

#     def print_bunbong(self, code: str):
#         self.SetInputValue("종목코드", code)
#         self.SetInputValue("틱범위", "30")
#         self.SetInputValue("수정주가구분", "0")
#         self.dynamicCall("CommRqData(QString, QString, int, QString)", "30분봉", "opt10080", 0, "2000")

#     def slot(self):
#         self.OnEventConnect.connect(self.login_slot)
#         self.OnReceiveRealData.connect(self.recv)
#         self.OnReceiveTrData.connect(self.tr_data)

#     def tr_data(self, sScrNo: str, sRQName: str, sTrCode: str,
#                 sRecordName: str, sPrevNext: str):

#         data = []
#         for i in range(50):
#             candle = {
#                 "고가": self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, "고가"),
#                 "저가": self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, "저가"),
#                 "시가": self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, "시가")
#             }
#             data.append(candle)

#         print("=============== 종목 코드: " + sTrCode)
#         index = 0
#         for i in data:
#             print(index)
#             print("고가: " + i["고가"])
#             print("저가: " + i["저가"])
#             print("시가: " + i["시가"])
#             print()
#             index += 1

#         self.global_event_loop.exit()

#     def recv(self, sCode, sRealType, sRealData):
#         print(sCode)
#         print(sRealData)
#         print(sRealType)

#     def signal_login_commConnect(self):
#         self.dynamicCall("CommConnect()")
#         self.login_event_loop.exec_()

#     def login_slot(self, err_code):
#         print("로그인 성공")

#         self.login_event_loop.exit()


# class Main():
#     def __init__(self):
#         print("Main() start")

#         self.app = QApplication(sys.argv)
#         self.kiwoom = Test()
#         self.app.exec_()
#         print("hi")


# if __name__ == "__main__":
#     Main()

from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop, pyqtSlot, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLayoutItem, QTextEdit, QLCDNumber
from PyQt5.QtGui import *
from PyQt5 import uic
import sys


class Test(QAxWidget):
    def __init__(self):
        super().__init__()

        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")  # 레지스트리에 저장된 api 모듈 불러오기
        self.login_event_loop = QEventLoop()
        self.slot_reg()
        self.signal_login_commConnect()

        self.global_event_loop = QEventLoop()

        self.candle_data: list

    def print_bunbong(self, code: str):
        self.SetInputValue("종목코드", code)
        self.SetInputValue("틱범위", "30")
        self.SetInputValue("수정주가구분", "0")
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "30분봉", "opt10080", 0, "2000")

    def slot_reg(self):
        self.OnEventConnect.connect(self.login_slot)
        # self.OnReceiveRealData.connect(self.recv)
        self.OnReceiveTrData.connect(self.tr_data)

    def tr_data(self, sScrNo: str, sRQName: str, sTrCode: str,
                sRecordName: str, sPrevNext: str):

        self.candle_data = []
        for i in range(6):
            candle = {
                "고가": self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, "고가"),
                "저가": self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, "저가"),
                "시가": self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, "시가"),
                "체결시간": self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, "체결시간")
            }
            self.candle_data.append(candle)

        self.global_event_loop.exit()

    def recv(self, sCode, sRealType, sRealData):
        print(sCode)
        print(sRealData)
        print(sRealType)

    def signal_login_commConnect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()

    def login_slot(self, err_code):
        print("로그인 성공")

        self.login_event_loop.exit()

    def get_candle_data(self, code: str) -> list:
        self.SetInputValue("종목코드", code)
        self.SetInputValue("틱범위", "30")
        self.SetInputValue("수정주가구분", "0")
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "30분봉", "opt10080", 0, "2000")
        self.global_event_loop.exec_()
        return self.candle_data


class GUI(QMainWindow):
    def __init__(self, kiwoom: Test):
        super().__init__()
        self.kiwoom = kiwoom
        self.ui = uic.loadUi("./test/test.ui", self)

        self.show()
        self.vBox = self.verticalLayout
        self.temp = price_now(self, self.kiwoom)

    def get_stock_code(self) -> str:
        self.stock_code: QTextEdit
        return self.stock_code.toPlainText()

    @pyqtSlot()
    def refreshCandle(self):
        candle_data = self.kiwoom.get_candle_data(self.get_stock_code())
        self.temp.reg()

        child = self.vBox.children()

        i = 1
        j = 0
        for grid in child:
            time = str(candle_data[j]["체결시간"])
            print(time)
            t_str = time[6:10] + "년 " + time[10:12] + "월 " + time[12:14] + "일 " + time[14:16] + "시 " + time[16:18] + "분 "
            self.findChild(QLabel, "l{}".format(i)).setText(t_str)
            i += 1
            self.findChild(QLabel, "l{}".format(i)).setText(candle_data[j]["시가"])
            i += 1
            self.findChild(QLabel, "l{}".format(i)).setText(candle_data[j]["고가"])
            i += 1
            self.findChild(QLabel, "l{}".format(i)).setText(candle_data[j]["저가"])
            i += 1
            j += 1


class price_now():
    def __init__(self, gui: GUI, kiwoom: Test):
        self.gui = gui
        self.kiwoom = kiwoom

        self.kiwoom.OnReceiveRealData.connect(self.real_data_slot)

    def reg(self):
        self.kiwoom.dynamicCall("SetRealReg(QString, QString, QString, QString)", "3000", self.gui.get_stock_code(), "10;12", 0)
        print("Fdsf")

    def real_data_slot(self, sCode: str, sRealType: str, sRealData: str):
        price = self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 10)
        percent = self.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, 12)
        print(price, percent)

        self.gui.price_label: QLabel
        self.gui.percent_label: QLabel

        self.gui.price_label.setText(price)
        self.gui.percent_label.setText(percent + "%")


class Main():
    def __init__(self):
        print("Main() start")

        self.app = QApplication(sys.argv)
        self.kiwoom = Test()
        self.ex = GUI(self.kiwoom)
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    Main()
