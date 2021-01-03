from PyQt5.QtCore import QEventLoop
from PyQt5.QAxContainer import QAxWidget
from config.errorCode import errors


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        print("Kiwoom() class start.")

        # event loop를 실행하기 위한 변수 모음
        self.login_event_loop = QEventLoop()
        self.detail_account_info_event_loop = None

        self.screen_my_info = "2000"
        self.use_money_percent = 0.5

        # 초기 셋팅 함수들 바로 실행
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")  # 레지스트리에 저장된 api 모듈 불러오기
        self.event_slots()
        self.signal_login_commConnect()
        self.get_account_info()
        self.detail_account_info()
        self.detail_account_my_stock()

    def get_account_info(self):
        account_list = self.dynamicCall("GetLoginInfo(QSting)", "ACCNO")
        account_num = account_list.split(";")[0]

        self.account_num = account_num

        print("계좌번호 : %s" % account_num)

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)
        self.OnReceiveTrData.connect(self.trdata_slot)

    def signal_login_commConnect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()

    def login_slot(self, err_code):
        print(errors(err_code)[1])

        self.login_event_loop.exit()

    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        print(sRQName)
        if sRQName == "예수금상세현황요청":
            deposit = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "예수금")
            self.deposit = int(deposit)

            use_money = float(self.deposit) * self.use_money_percent
            self.use_money = int(use_money)
            self.use_money = self.use_money / 4

            output_deposit = self.dynamicCall("GetCommData(Qstring, QString, int, QString)", sTrCode, sRQName, 0, "출금가능금액")
            self.output_deposit = int(output_deposit)

            print("예수금 : %s" % self.output_deposit)

            self.stop_screen_cancel(self.screen_my_info)
            self.detail_account_info_event_loop.exit()
        elif sRQName == "계좌평가잔고내역요청":
            total_buy_money = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총매입금액")
            self.total_buy_money = int(total_buy_money)

            total_profit_loss_money = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총평가손익금액")
            self.total_profit_loss_money = float(total_profit_loss_money)

            total_profit_loss_rate = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총수익률(%)")
            self.total_profit_loss_rate = float(total_profit_loss_rate)

            print("계좌평가잔고내역요청 싱글데이터: %s - %s - %s", (total_buy_money, total_profit_loss_money, total_profit_loss_money))

    def stop_screen_cancel(self, sScrNo=None):
        self.dynamicCall("DisconnectRealData(QString)", sScrNo)

    def detail_account_info(self, sPrevNext=0):
        self.setInputValue("계좌번호", self.account_num)
        self.setInputValue("비밀번호", "0000")
        self.setInputValue("비밀번호입력매체구분", "00")
        self.setInputValue("조회구분", "2")

        self.dynamicCall("CommRqData(QString, QString, int, QString)", "예수금상세현황요청", "opw00001", sPrevNext, self.screen_my_info)
        self.detail_account_info_event_loop = QEventLoop()
        self.detail_account_info_event_loop.exec_()

    def detail_account_my_stock(self, sPrevNext=0):
        self.setInputValue("계좌번호", self.account_num)
        self.setInputValue("비밀번호", "0000")
        self.setInputValue("비밀번호입력매체구분", "00")
        self.setInputValue("조회구분", "1")
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "계좌평가잔고내역요청", "opw00018", sPrevNext, self.screen_my_info)

    def setInputValue(self, param1, param2):
        self.dynamicCall("SetInputValue(QString, QString)", param1, param2)
