from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop

from request.enum.stockEnum import TrCode


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

    __global_eventloop = None       # 동기처리를 위한 전역 EventLoop
    __tr_data_temp = {}             # GetTrData의 결과가 임시적으로 담기는 곳
    __condition_name_list = []      # 조건식 이름과 인덱스가 임시적으로 담기는 곳
    __condition_stock_list = None   # 조건식 필터링 결과가 임시적으로 담기는 곳
    __tr_rq_single_data = None      # 사용자 요청 싱글데이터
    __tr_rq_multi_data = None       # 사용자 요청 멀티데이터
    __realtime_data_callback = None     # 실시간 데이터 콜백

    def __init__(self):
        self.__global_eventloop = QEventLoop()
        self.__reg_all_slot()     # 이벤트 슬롯 등록

    def get_tr_data(self, inputValue: dict, trEnum: TrCode, nPrevNext: int, sScrNo: str, rqSingleData, rqMultiData):
        '''
        키움 API에 Tr 데이터를 요청한다.
        '''
        self.__tr_rq_single_data = rqSingleData
        self.__tr_rq_multi_data = rqMultiData

        self.set_input_values(inputValue)   # inputvalue 대입
        self.dynamicCall("CommRqData(Qstring, QString, int, QString)",
                         trEnum.value, trEnum.name, nPrevNext, sScrNo)
        self.__global_eventloop.exec_()
        return self.__tr_data_temp

    def get_condition_list(self):
        '''
        키움 증권 HTS에 저장되어 있는 조건식을 반환

        return value
        ------------
        [
            [인덱스번호, 조건식 이름],
            [인덱스번호, 조건식 이름],
            ...
        ]
        '''
        self.dynamicCall("GetConditionLoad()")
        self.__global_eventloop.exec_()
        return self.__condition_name_list

    def get_condition_stock(self, sScrNo, index, cond_name):
        '''
        해당 조건식을 만족하는 종목 코드를 리스트 형태로 반환

        param
        -------
        index: 조건식 인덱스 번호

        cond_name: 조건식 이름
        '''
        self.dynamicCall("SendCondition(QString, QString, int, int)", sScrNo, cond_name, index, 0)
        self.__global_eventloop.exec_()
        return self.__condition_stock_list

    def set_realtime_reg(self, sScrNo: str, stockList, realtimeDataList):
        '''
        realtime data를 받아올 수 있도록 레지스터링 한다.

        param
        -----------
        stockList = [Stock, Stock, ...] # Stock 객체가 list 형태로 들어와야함

        realTimeDataList = [RealTimeDataEnum, ...] # RealTimeDataEnum 객체가 list 형태로 들어와야함
        '''
        if self.__realtime_data_callback is None:
            raise RuntimeError("realtime data callback 함수가 설정되지 않았습니다.")

        fid_list = "".join("{};".format(fid.value) for fid in realtimeDataList)[:-1]  # fid str list
        stock_code_list = "".join("{};".format(stock.get_code_name()) for stock in stockList)[:-1]  # stock code str list

        self.dynamicCall("SetRealReg(QString, QString, QString, QString)", sScrNo, stock_code_list,
                         fid_list, 1)

    def set_realtime_callback(self, callback):
        self.__realtime_data_callback = callback

    def _set_input_values(self, input_value: dict):
        '''
        SetInputVlaue() 동적 호출 iteration 용도
        '''
        for k, v in input_value.items():
            self.dynamicCall("SetInputValue(QString, QString)", k, v)

    def _tr_data_slot(self, sScrNo, sTrCode, sRecordName, sPrevNext):
        '''
        CommRqData 처리용 슬롯
        '''
        self.__tr_data_temp.clear()     # 이전에 저장되어 있던 임시 tr_data 삭제.

        self.__tr_data_temp["single_data"] = {}     # empty dict 선언
        for s_data in self.__tr_rq_single_data:
            self.__tr_data_temp["single_data"][s_data] = self.dynamicCall(
                "GetCommData(QString, QString, int, QString)", sScrNo, sTrCode, 0, s_data)

        self.__tr_data_temp["multi_data"] = {}      # empty dict 선언
        for i in range(500):
            for m_data in self.__tr_rq_multi_data:
                self.__tr_data_temp["multi_data"][m_data] = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sScrNo, sTrCode, i, m_data)

        self.__global_eventloop.exit()

    def _realtime_data_slot(self, sCode, sRealType, sRealData):
        '''
        realtime data 처리용 슬롯
        '''
        self.__realtime_data_callback(sCode, sRealType, sRealData)

    def _send_condition_slot(self, sScrNo, strCodeList, strConditionName, nIndex, nNext):
        '''
        SendCondition 처리용 슬롯
        '''
        self.__condition_stock_list = strCodeList[:-1].split(";")
        self.__event_loop.exit()

    def _condition_ver_slot(self, lRet, sMsg):
        '''
        GetConditionLoad 처리용 슬롯
        '''
        self.__condition_name_list.clear()  # 이전에 저장되어 있던 조건식 들을 삭제한다.
        condition_name_list = self.__kiwoom.dynamicCall("GetConditionNameList()")

        '''
        condition_name_list 데이터 형태
        ==============
        인덱스^조건식이름;인덱스^조건식이름;
        '''

        for cond_index_name in condition_name_list[:-1].split(";"):
            self.__condition_list.append(cond_index_name.split("^"))

        self.__global_eventloop.exit()

    def __reg_all_slot(self):
        '''
        키움 API의 이벤트 슬롯을 전부 다 등록
        '''
        self.OnReceiveTrData.connect(self.__tr_data_slot)             # Tr 데이터 슬롯
        self.OnReceiveConditionVer.connect(self._condition_ver_slot)  # 조건식 데이터 슬롯
        self.OnReceiveTrCondition.connect(self._send_condition_slot)  # 조건식 종목 슬롯
        self.OnReceiveRealData.connect(self._realtime_data_slot)      # 실시간 데이터 슬롯
