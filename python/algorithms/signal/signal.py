from PyQt5.QtCore import QThread
from algorithms.condition import Condition
from request.dao import Dao
from request.enum.stockEnum import OfferStock


class Signal(QThread):
    '''
    시그널 감지 클래스
    '''
    __condition_list = []

    def __init__(self):
        pass

    def run(self):
        pass

    def attach_signal(self, condition: Condition, offer) -> None:
        '''
        시그널 이벤트 등록
        '''
        Dao().reg_slot(self.real_data_slot)
        self.__condition_list.append([
            condition, offer
        ])

    def detach_signal(self):
        pass

    def get_signal_list(self):
        pass

    def real_data_slot(self, sScrNo: str, sRQName: str, sTrCode: str, sRecordName: str, sPrevNext: str):
        '''
        real time data 이벤트 슬롯

        attribute
        ---------
          BSTR sScrNo,       // 화면번호
          BSTR sRQName,      // 사용자 구분명
          BSTR sTrCode,      // TR이름
          BSTR sRecordName,  // 레코드 이름
          BSTR sPrevNext,    // 연속조회 유무를 판단하는 값 0: 연속(추가조회)데이터 없음, 2:연속(추가조회) 데이터 있음
        '''
        # TODO DAO를 호출해서 GetCommRQData를 받아와야함
        # TODO realtime data 를 가공해야함

        self.run_condition_trade()

    def run_condition_trade(self, index: int, realtime_data):
        condition_value, offer = self.check_condition(index, realtime_data)
        if condition_value:
            # 조건 충족
            if offer == OfferStock.BUYING:
                # 매수 조건일 때
                Dao().buy_stock()
            else:
                # 매도 조건일 때
                Dao().sell_stock()

    def check_condition(self, index: int, realtime_data) -> bool:
        '''
        조건 판별
        '''
        condition: Condition
        condition = self.__condition_list[index][0]
        return (condition.condition(realtime_data), self.__condition_list[index][1]
