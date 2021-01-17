from typing import Any, Dict, List

from algorithms.algorithm import Algorithm
from algorithms.condition import Condition
from entity.stock import Stock
from request.dao import Dao
from request.enum.stockEnum import CandleUnit, RealTimeDataEnum


class fifteen_bottom(Algorithm):
    '''
    15분봉 매매법
    '''

    dao: Dao
    def __init__(self, stock: Stock):
        super().__init__(stock, fifteen_bottom.fifteen_bottom_BuyingCondition, fifteen_bottom.fifteen_bottom_sellingCondition, 60)
        self.dao = Dao()
        # day = Dao().get_today_date()

    def filter_list(self) -> list:
        condition_list = Dao().request_condition_list()

        ready_stock = []

        for condition in condition_list:
            if condition[1] == "fifteen_bottom":
                stock_list: List[Stock] = Dao().request_condition_stock(condition[0], condition[1])
        for stock in stock_list:
            find_stock = Dao().request_stock_instance(stock)
            data = Dao().request_candle_data(find_stock, CandleUnit.MINUTE, 30)  #한번만 검색하면됨.
            if data.loc[0].percentage >= 3:
                ready_stock.append(stock)
                Dao().set_buying_price(stock, data.loc[0].open)
        return ready_stock

    class fifteen_bottom_BuyingCondition(Condition):
        def condition_test(self, stock: Stock, realtime_data: Dict[RealTimeDataEnum, Any]):
            '''
            Condition 클래스의 condition 메소드를 오버라이드
            만약
            '''
            rtde = RealTimeDataEnum
            current_price = realtime_data[rtde.CURRENT_PRICE]
            buying_price = Dao().request_buying_price(stock.get_code_name())
            if current_price == buying_price:
                Dao().store_stock(stock)
                return True

            return False


    class fifteen_bottom_sellingCondition(Condition):
        def condition_test(self, stock: Stock, realtime_data: Dict[RealTimeDataEnum, Any]):
            '''
            Condition 클래스의 condition 메소드를 오버라이드
            '''
            rtde = RealTimeDataEnum
            current_price = realtime_data[rtde.CURRENT_PRICE]
            buying_price = Dao().request_buying_price(stock.get_code_name())
            data = Dao().request_candle_data_from_now(stock.get_code_name(), CandleUnit.MINUTE, 30)
            if (((current_price - buying_price) - 1) * 100) > 0.8:
                Dao().delete_stock()
                return True
            elif data.loc[0].close < buying_price:
                Dao().delete_stock()
                return True
            return False
