import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop


class ang(QAxWidget):
    def __init__(self):
        # print("kiwoom() class start")
        print("hello")
        super().__init__()
        self.login_event_loop = None

        self.all_stock_dict = {}

        self.account_stock_dict = {}
        self.not_account_stock_dict = {}

        self.portfolio_stock_dict = {}
        self.jango_dict = {}

        self.calcul_data = []

        self.screen_start_stop_real = "1000"

        self.get_ocx_instance()
        self.event_slots()
        self.signal_login_commConnect()

        self.condition_event_slot()
        self.condition_signal()

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

    def condition_event_slot(self):
        self.OnReceiveConditionVer.connect(self.condition_slot)
        self.OnReceiveTrCondition.connect(self.condition_tr_slot)
        # self.OnReceiveRealCondition.connect(self.condition_real_slot)

    def get_condition_list(self):
        pass

    def condition_slot(self, ConditionName):

        condition_name_list = self.dynamicCall("GetConditionNameList()")

        condition_name_list = condition_name_list.split(";")[:-1]

        for unit_condition in condition_name_list:
            index = unit_condition.split("^")[0]
            index = int(index)
            condition_name = unit_condition.split("^")[1]
        if condition_name == ConditionName:
            self.dynamicCall("SendCondition(QString, QString, int, int)",
                             "0156", condition_name, index, 0)  # 조회요청 + 실시간 조회print("조회 성공여부 %s " % ok)


    def condition_signal(self):
        self.dynamicCall("GetConditionLoad()")

    # 나의 조건식에 해당하는 종목코드 받기
    def condition_tr_slot(self, sScrNo, strCodeList, strConditionName, index, nNext):
        print("화면번호: %s, 종목코드 리스트: %s, 조건식 이름: %s, 조건식 인덱스: %s, 연속조회: %s" % (sScrNo, strCodeList, strConditionName, index, nNext))

        code_list = strCodeList.split(";")[:-1]
        print("코드 종목 \n %s" % code_list)
        return code_list
