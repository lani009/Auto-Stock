from algorithms.algorithm import Algorithm
from algorithms.condition import Condition
from entity.stock import Stock
from request.dao import Dao
from request.enum.stockEnum import CandleUnit
from algorithms.signal.signal import Signal


class Ma_Discrepancy(Algorithm):
    '''
    15분봉 매매법
    '''
    dao: Dao
    def __init__(self, stock: Stock):
        super().__init__(stock, Ma_Discrepancy.Ma_Discrepancy_BuyingCondition, Ma_Discrepancy.Ma_Discrepancy_sellingCondition)
        self.dao = Dao()

    def filter_list(self) -> list:
        condition_list = Dao().reqest_condition_list()

        for condition in condition_list:
            if condition[1] == "해당"
            requsetr condition sotck

            for
            상승추세 분간 

        return stock

    class Ma_Discrepancy_BuyingCondition(Condition):
        def __init__(self):
            super().__init__()

        def condition_test(self):
            '''
            Condition 클래스의 condition 메소드를 오버라이드
            만약 
            '''
            request candle data 
            data = > d이평선 불러와서


            if stock.realtime <= 특정 이평선 값 && 기울기 




    class Ma_Discrepancy_sellingCondition(Condition):
        def __init__(self):
            super().__init__()

        def condition_test(self):
            '''
            Condition 클래스의 condition 메소드를 오버라이드
            '''
            pass
