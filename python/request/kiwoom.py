from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop


class Kiwoom(QAxWidget):
    '''
    키움 통신 클래스
    =============
    키움 API와 직접적인 통신을 진행한다.

    Thread_safe함.

    TODO
    -----------
    이벤트루프를 적용하여 get_tr_data 등의 메소드가 thread safe 해야함
    '''

    __tr_data_temp = None
    __global_eventloop = QEventLoop()

    def __init__(self):
        self.OnReceiveTrData.connect(self.tr_data_slot)

    def get_tr_data(self, input_value: dict, sRQName: str, sTrCode: str, nPrevNext: int, sScreenNo: str):
        self.set_input_values(input_value)
        self.dynamicCall("CommRqData(Qstring, QString, int, QString)", sRQName, sTrCode, nPrevNext, sScreenNo)
        self.__global_eventloop.exec_()
        return self.__tr_data_temp

    def _set_input_values(self, input_value: dict):
        for k, v in input_value.items():
            self.dynamicCall("SetInputValue(QString, QString)", k, v)

    def _tr_data_slot(self):
        self.__tr_data_temp = None
        self.__global_eventloop.exit()

"""
tr data
opt10001 주식기본정보요청 -> 종목코드/ 종목명
opt10080 주식분봉차트조회요청 -> 거래량 / 시가 / 고가 / 저가


Real Type
주식 시세 -> 10 현재가/ 12 등락율 / 16 시가 / 17 고가/ 18 저가
주식 호가 잔량 -> 121 매도호가총잔량 / 125 매수호가총잔량
"""
