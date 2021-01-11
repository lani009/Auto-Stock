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
    __tr_data_temp = None           # GetTrData의 결과가 임시적으로 담기는 곳
    __condition_name_list = []      # 조건식 이름과 인덱스가 임시적으로 담기는 곳
    __condition_stock_list = None   # 조건식 필터링 결과가 임시적으로 담기는 곳

    def __init__(self):
        self.__global_eventloop = QEventLoop()
        self.__reg_all_slot()     # 이벤트 슬롯 등록

    def get_tr_data(self, input_value: dict, trEnum: TrCode, nPrevNext: int, sScreenNo: str):
        '''
        키움 API에 Tr 데이터를 요청한다.
        '''
        self.set_input_values(input_value)
        self.dynamicCall("CommRqData(Qstring, QString, int, QString)", trEnum.value, trEnum.value, nPrevNext, sScreenNo)
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
        ------
        index: 조건식 인덱스 번호

        cond_name: 조건식 이름
        '''
        self.dynamicCall("SendCondition(QString, QString, int, int)", sScrNo, cond_name, index, 0)
        self.__global_eventloop.exec_()
        return self.__condition_stock_list

    def _set_input_values(self, input_value: dict):
        '''
        SetInputVlaue() 동적 호출 용도
        '''
        for k, v in input_value.items():
            self.dynamicCall("SetInputValue(QString, QString)", k, v)

    def _tr_data_slot(self):
        '''
        CommRqData 처리용 슬롯
        '''
        self.__tr_data_temp = None  # TODO
        self.__global_eventloop.exit()

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
