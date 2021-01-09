from abc import ABCMeta, abstractmethod


class Condition(metaclass=ABCMeta):
    '''
    매수, 매도 시점에 대한 조건식
    '''
    def __init__():
        pass

    @abstractmethod
    def condition_test(self, realtime_data: dict) -> bool:
        """
        docstring
        """
        raise NotImplementedError
