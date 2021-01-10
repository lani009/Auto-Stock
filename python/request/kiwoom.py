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
    __condition_list = None
    ___found_code_list = None


    def __init__(self):
        self.OnReceiveTrData.connect(self.tr_data_slot)
        self.OnReceiveConditionVer.connect(self.condition_slot)
        self.OnReceiveTrCondition.connect(self.condition_tr_slot)
        self.condition_signal()

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

###########################################################################################
    def condition_signal(self):
        self.dynamicCall("GetConditionLoad()")

    def get_condition_list(self):

        condition_name_list = self.dynamicCall("GetConditionNameList()")
        self.__condition_list = condition_name_list
        return self.__condition_list


    def _condition_slot(self, lRet, sMsg):
        
        self.get_condition_list()


    def get_condition_stock_code(ConditionName):

        condition_name_list = __condition_list.split(";")[:-1]

        for unit_condition in condition_name_list:
            index = unit_condition.split("^")[0]
            index = int(index)
            condition_name_list = unit_condition.split("^")[1]
            if condition_name_list == ConditionName:
                self.dynamicCall("SendCondition(QString, QString, int, int)",
                                 "0156", ConditionName, index, 0)  # 조회요청 + 실시간 조회print("조회 성공여부 %s " % ok)


    def _condition_tr_slot(self, sScrNo, strCodeList, strConditionName, index, nNext):
        print("화면번호: %s, 종목코드 리스트: %s, 조건식 이름: %s, 조건식 인덱스: %s, 연속조회: %s" % (sScrNo, strCodeList, strConditionName, index, nNext))
        code_list = strCodeList.split(";")[:-1]
        print("코드 종목 \n %s" % code_list)



    def get_condition_list(self):
        return self.__condition_name_list



"""
tr data
opt10001 주식기본정보요청 -> 종목코드/ 종목명
opt10080 주식분봉차트조회요청 -> 거래량 / 시가 / 고가 / 저가


Real Type
주식 시세 -> 10 현재가/ 12 등락율 / 16 시가 / 17 고가/ 18 저가
주식 호가 잔량 -> 121 매도호가총잔량 / 125 매수호가총잔량
"""
