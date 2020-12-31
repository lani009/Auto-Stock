from PyQt5.QtCore import *
from PyQt5.QAxContainer import QAxWidget
from config.errorCode import errors
class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        print("Kiwoom() class start.")

        
        # event loop를 실행하기 위한 변수 모음
        self.login_event_loop = QEventLoop()
        
        # 초기 셋팅 함수들 바로 실행
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")    # 레지스트리에 저장된 api 모듈 불러오기
        self.event_slots()
        self.signal_login_commConnect()

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)

    def signal_login_commConnect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()

    def login_slot(self, err_code):
        print(errors(err_code)[1])

        self.login_event_loop.exit()