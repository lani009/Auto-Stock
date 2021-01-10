from algorithms.algorithm import Algorithm
from algorithms.condition import Condition
from entity.stock import Stock
from request.dao import Dao
from request.enum.stockEnum import CandleUnit
from algorithms.signal.signal import Signal


class Fifteen_Pivot2(Algorithm):
    '''
    15분봉 매매법
    '''

    def __init__(self, stock: Stock):
        super().__init__(stock, Fifteen_Pivot2.Fifteen_Pivot2_BuyingCondition, Fifteen_Pivot2.Fifteen_Pivot2_sellingCondition)

    class Fifteen_Pivot2_BuyingCondition(Condition):
        def __init__(self):
            super().__init__()

        def filter_list(self) -> [Stock, ...]:
            stock_box = Dao.put_found_stock("")
                
        def condition_test(self):
            '''
            Condition 클래스의 condition 메소드를 오버라이드
            '''
            pass

    class Fifteen_Pivot2_sellingCondition(Condition):
        def __init__(self):
            super().__init__()

        def condition_test(self):
            '''
            Condition 클래스의 condition 메소드를 오버라이드
            '''
            pass
