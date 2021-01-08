from abc import abstractmethod, ABCMeta
from algorithms.condition import Condition
from entity.stock import Stock


class Algorithm(metaclass=ABCMeta):
    '''
    주식 거래 알고리즘 추상클래스
    ===========

    attribute
    ---------
    Algorithm 클래스 하나는 오직 한개의 종목만 거래할 수 있다.
    '''
    __stock: Stock  # 보유 주식
    __money: int    # 예수금
    __selling_condition: Condition  # 매도 조건
    __buying_condition: Condition   # 매수 조건

    def __init__(self):
        pass

    @abstractmethod
    @staticmethod
    def filter_list(self):
        '''
        거래 대상 주식 필터링
        '''
        pass

    def force_selling(self):
        '''
        보유 주식 강제매도
        '''
        pass

    def moderate_selling(self):
        '''
        상황 봐가면서 매도하는 메소드

        되도록이면 매도하되, 이건 좀 아니다 싶으면 홀딩한다.
        '''
        pass
