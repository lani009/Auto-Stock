from typing import Any, Dict
from algorithms.algorithm import Algorithm
from algorithms.condition import Condition
from entity.stock import Stock
from request.dao import Dao
from request.enum.stockEnum import CandleUnit
from algorithms.signal.signal import Signal
from request.enum.stockEnum import RealTimeDataEnum

class fifteen_bottom(Algorithm):
    '''
    15분봉 매매법
    '''

    dao: Dao
    def __init__(self, stock: Stock):
        super().__init__(stock, fifteen_bottom.fifteen_bottom_BuyingCondition, fifteen_bottom.fifteen_bottom_sellingCondition)
        self.dao = Dao()
        day = Dao().get_today_date()

    def filter_list(self) -> list:
        condition_list = Dao().request_condition_list()

        for condition in condition_list:
            if condition[1] == "fifteen_bottom":
                stock_list = Dao().request_condition_stock(condition[0], condition[1])
        for stock in stock_list:
            find_stock = Dao().request_stock_instance(stock)
            data = Dao.request_candle_data(find_stock, CandleUnit.MINUTE, 15)  #한번만 검색하면됨.
            if data.loc[0].percentage > 3 or data.loc[1].percentage > 3:
                self.ready_stock.append(stock)
                
        return self.ready_stock

    class fifteen_bottom_BuyingCondition(Condition):
        def __init__(self):
            super().__init__()

        def condition_test(self, stock: Stock, realtime_data: Dict[RealTimeDataEnum, Any]):
            '''
            Condition 클래스의 condition 메소드를 오버라이드
            만약
            '''

            detect_stock = Dao().request_stock_instance(stock)
            data = Dao().request_candle_data(detect_stock, CandleUnit.MINUTE, 15)
            for i in data.percentage:
                if i>3:

            

            rtde = RealTimeDataEnum
            current_price = realtime_data[rtde.CURRENT_PRICE]  # 현재가 
            if 



    class fifteen_bottom_sellingCondition(Condition):
        def __init__(self):
            super().__init__()

        def condition_test(self):
            '''
            Condition 클래스의 condition 메소드를 오버라이드
            '''
            pass
