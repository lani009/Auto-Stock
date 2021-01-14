from abc import ABCMeta, abstractmethod


class Condition(metaclass=ABCMeta):
    '''
    매수, 매도 시점에 대한 조건식
    '''
    def __init__(self):
        pass

    @abstractmethod
    def condition_test(self, realtime_data: dict) -> bool:
        """
        조건 검색 실행
        """
        raise NotImplementedError

    @abstractmethod
    def realtime_data_requirement(self):
        '''
        REALTIME 데이터 중 필요로하는 데이터에 대한 정의
        '''
        raise NotImplementedError
