from abc import ABCMeta, abstractmethod


class Condition(metaclass=ABCMeta):
    '''
    매수, 매도의 조건
    '''
    def __init__():
        pass

    @abstractmethod
    def condition(self, realtime_data: dict):
        """
        docstring
        """
        raise NotImplementedError
