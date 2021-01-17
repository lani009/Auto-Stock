from typing import Any, Dict, List, Tuple
from AutoStock.request.enum.stockEnum import RealTimeDataEnum
from AutoStock.request.dao import Dao
from AutoStock.request.enum.stockEnum import OfferStock
from PyQt5.QtCore import QThread, QWaitCondition
from AutoStock.algorithms.condition import Condition
from AutoStock.entity.stock import Stock

class Signal(QThread):
    '''
    시그널 감지 클래스
    '''
    __refresh_time: int = None  # 조건 새로고침 주기 단위(초)
    __condition_list: List[Tuple[Condition, OfferStock]]   # condition 목록
    __realtime_data_temp = None
    __stock: Stock = None     # 할당 받은 주식 종목

    def __init__(self, refresh_time, stock):
        self.__refresh_time = refresh_time
        self.__stock = stock

    def run(self):
        while True:
            if self.__realtime_data_temp is not None:
                self.run_condition_trade(0, self.__realtime_data_temp)
                self.run_condition_trade(1, self.__realtime_data_temp)
            QWaitCondition.wait(self.__refresh_time)

    def attach_condition(self, condition: Condition, offer: OfferStock) -> None:
        '''
        시그널 이벤트 등록
        '''
        # Dao에서 실시간 데이터를 받아올 수 있도록 함.
        Dao().reg_realtime_data(self.realtime_data_slot, self.__stock, condition.realtime_data_requirement())    # 실시간 슬롯에 등록
        self.__condition_list.append([condition, offer])

    def detach_condition(self):
        pass

    def get_condition_list(self) -> List[Tuple[Condition, OfferStock]]:
        return self.__condition_list

    def realtime_data_slot(self, realtime_data: Dict[RealTimeDataEnum, Any]):
        '''
        real time data 이벤트 슬롯

        attribute
        ---------
          realtime_data: 실시간 데이터
        '''
        self.__realtime_data_temp = realtime_data
        # TODO 현재 상황에 맞추어 매도, 매수 조건 중 무엇을 감시할 지 설정
        self.run_condition_trade(self.index, self.__realtime_data_temp)

    def run_condition_trade(self, index: int, realtime_data):
        '''
        매도 매수 조건이 만족될 경우, 거래를 진행시킨다.
        '''
        condition_value, offer = self._check_condition(index, realtime_data)
        if condition_value:
            # 조건 충족
            if offer == OfferStock.BUYING:
                # 매수 조건일 때
                Dao().buy_stock()
            else:
                # 매도 조건일 때
                Dao().sell_stock()

    def _check_condition(self, index: int, realtime_data):
        '''
        매도, 매수 조건에 맞는지 판별
        '''
        condition = self.__condition_list[index][0]
        return (condition.condition_test(self.__stock, realtime_data), self.__condition_list[index][1])
