from algorithms.algorithm import Algorithm
from algorithms.condition import Condition
from entity.stock import Stock


class FifteenCandel(Algorithm):
    '''
    15분봉 매매법
    '''
    def __init__(self, stock: Stock, buying_condition: Condition, selling_condition: Condition):
        super().__init__(stock, buying_condition, selling_condition)


class FifteenCandel_BuyingCondition(Condition):
    def __init__(self):
        super().__init__()

    def condition(self):
        '''
        Condition 클래스의 condition 메소드를 오버라이드
        '''
        pass


class FifteenCandel_sellingCondition(Condition):
    def __init__(self):
        super().__init__()

    def condition(self):
        '''
        Condition 클래스의 condition 메소드를 오버라이드
        '''
        pass
