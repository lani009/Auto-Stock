from PyQt5.QtCore import QEventLoop
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtWidgets import QApplication
import sys
import time


class Main():
    __kiwoom = None
    __event_loop = None
    __condition_list = []
    __condition_stock_list = []
    __tr_data_temp = None
    __tr_rq_single_data = None
    __tr_rq_multi_data = None

    def __init__(self):
        self.__kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.__event_loop = QEventLoop()

        self.__kiwoom.OnEventConnect.connect(self.__login_slot)
        self.__kiwoom.OnReceiveConditionVer.connect(self.__condition_ver_slot)
        self.__kiwoom.OnReceiveTrCondition.connect(self.__send_condition_slot)
        self.__kiwoom.OnReceiveTrData.connect(self.__tr_data_slot)
        self.__kiwoom.OnReceiveRealData.connect(self.__realtime_slot)

    def login(self):
        self.__kiwoom.dynamicCall("CommConnect()")
        self.__event_loop.exec_()

    def get_realtime_data(self):
        self.__kiwoom.dynamicCall("SetRealReg(QString, QString, QString, QString)", "2000", "139480", "10", "0")

    def get_condition_list(self):
        self.__kiwoom.dynamicCall("GetConditionLoad()")
        self.__event_loop.exec_()
        return self.__condition_list

    def print_condition_list(self, cond):
        self.__kiwoom.dynamicCall("SendCondition(QString, QString, int, int)", "2000", cond[1], cond[0], 0)
        self.__event_loop.exec_()

        print("{} 조건식의 검색 결과".format(cond[1]))
        i = 1
        for stock in self.__condition_stock_list:
            print("{} ".format(stock), end="")
            if i % 10 == 0:
                print()
            i += 1

    def get_tr_data(self, inputValue: dict, sRQName: str, sTrName: str, nPrevNext: int, sScreenNo: str, rqSingleData, rqMultiData):
        '''
        키움 API에 Tr 데이터를 요청한다.
        '''
        self.__tr_rq_single_data = rqSingleData
        self.__tr_rq_multi_data = rqMultiData

        self.set_input_values(inputValue)   # inputvalue 대입
        self.dynamicCall("CommRqData(Qstring, QString, int, QString)", sRQName, sTrName, nPrevNext, sScreenNo)
        self.__event_loop.exec_()
        return self.__tr_data_temp

    def _set_input_values(self, input_value: dict):
        '''
        SetInputVlaue() 동적 호출 iteration 용도
        '''
        for k, v in input_value.items():
            self.dynamicCall("SetInputValue(QString, QString)", k, v)

    def __realtime_slot(self, sCode, sRealType, sRealData):
        '''
        realtype: 한글 FID 이름
        '''
        # print(sRealData, "j")
        print(self.__kiwoom.dynamicCall("GetCommRealData(QString ,int)", sCode, 10))

    def __condition_ver_slot(self, lRet, sMsg):
        condition_name_list: str
        condition_name_list = self.__kiwoom.dynamicCall("GetConditionNameList()")
        '''
        condition_name_list
        ==============
        인덱스^조건식이름;인덱스^조건식이름;
        '''

        for cond_index_name in condition_name_list[:-1].split(";"):
            self.__condition_list.append(cond_index_name.split("^"))

        self.__event_loop.exit()

    def __login_slot(self, errNo):
        print(errNo)
        self.__event_loop.exit()

    def __send_condition_slot(self, sScrNo, strCodeList, strConditionName, nIndex, nNext):
        self.__condition_stock_list = strCodeList.split(";")
        self.__event_loop.exit()

    def __tr_data_slot(self, sScrno, sRQName, sTrCode, sRecodrName, sPrevNext):
        '''
        CommRqData 처리용 슬롯
        '''
        self.__tr_data_temp = None  # 이전에 저장되어 있던 임시 tr_data 삭제. 가비지 콜렉터를 믿는다.
        self.candle_data = []
        # for i in range(200):
        #     candle = {
        #         "고가": self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, "고가"),
        #         "저가": self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, "저가"),
        #         "시가": self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, "시가"),
        #         "체결시간": self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, "체결시간")
        #     }
        self.__event_loop.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.login()
    main.get_realtime_data()

    sys.exit(app.exec_())
