from typing import Any, Dict, List
from copy import deepcopy

from AutoStock.algorithms.algorithm import Algorithm
from AutoStock.algorithms.condition import Condition
from AutoStock.entity.stock import Stock
from AutoStock.request.dao import Dao
from AutoStock.request.enum.stockEnum import CandleUnit, RealTimeDataEnum


class FifteenBottom(Algorithm):
    '''
    15분봉 매매법
    '''

    __dao: Dao
    def __init__(self, stock: Stock):
        super().__init__(stock, FifteenBottom.FifteenBottom_BuyingCondition, FifteenBottom.FifteenBottom_SellingCondition, 60, 50000)
        self.__dao = Dao()
        # day = Dao().get_today_date()

    @staticmethod
    def filter_list() -> list:
        condition_list = Dao().request_condition_list()

        ready_stock = []

        for condition in condition_list:
            if condition[1] == "fifteen_bottom":
                stock_list: List[Stock] = Dao().request_condition_stock(condition[0], condition[1])
        for stock in stock_list:
            data = Dao().request_candle_data_from_now(stock, CandleUnit.MINUTE, 30)  #한번만 검색하면됨.
            if data.loc[0].percentage >= 3:
                ready_stock.append(stock)
                Dao().set_buying_price(stock, data.loc[0].open)
        return deepcopy(ready_stock)

    def moderate_selling(self):
        return super().moderate_selling()

    class FifteenBottom_BuyingCondition(Condition):
        def condition_test(self, stock: Stock, realtime_data: Dict[RealTimeDataEnum, Any]):
            '''
            Condition 클래스의 condition 메소드를 오버라이드
            만약
            '''
            rtde = RealTimeDataEnum
            current_price = realtime_data[rtde.CURRENT_PRICE]
            buying_price = Dao().request_buying_price(stock)
            if current_price == buying_price:
                # Dao().store_stock(stock)
                return True
            return False

        def realtime_data_requirement(self):
            return [RealTimeDataEnum.CURRENT_PRICE]


    class FifteenBottom_SellingCondition(Condition):
        def condition_test(self, stock: Stock, realtime_data: Dict[RealTimeDataEnum, Any]):
            '''
            Condition 클래스의 condition 메소드를 오버라이드
            '''
            rtde = RealTimeDataEnum
            current_price = realtime_data[rtde.CURRENT_PRICE]
            buying_price = Dao().request_buying_price(stock)
            data = Dao().request_candle_data_from_now(stock, CandleUnit.MINUTE, 30)
            if (((current_price - buying_price) - 1) * 100) > 0.8:
                # 익절
                # Dao().delete_stock()
                return True
            elif data.loc[0].close < buying_price:
                # 손절
                # Dao().delete_stock()
                return True
            return False

        def realtime_data_requirement(self):
            return [RealTimeDataEnum.CURRENT_PRICE]
