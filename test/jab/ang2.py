from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import QApplication
import sys


class Test(QAxWidget):
    ge = None
    def __init__(self):
        super().__init__()
        
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

        self.OnEventConnect.connect(self.login_slot)
        self.OnReceiveConditionVer.connect(self.ce_slot)
        self.dynamicCall("CommConnect()")
        self.ge = QEventLoop()
        self.ge.exec_()
        
        self.dynamicCall("GetConditionLoad()")


    def ce_slot(self, f, a):
        print(self.dynamicCall("GetConditionNameList()"))

    def login_slot(self, a):
        self.ge.exit()

if __name__ == "__main__":
    a = QApplication(sys.argv)
    Test()
    sys.exit(a.exec_())
