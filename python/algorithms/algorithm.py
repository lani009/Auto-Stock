from abc import abstractmethod, ABCMeta


class Algorithm(metaclass=ABCMeta):
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
