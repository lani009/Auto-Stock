from threading import Thread
from algorithms.condition import Condition


class Signal(Thread):
    '''
    시그널 감지 클래스
    '''
    def __init__(self):
        pass

    def run(self):
        pass

    def attach_signal(self, condition: Condition, callback: float) -> None:
        '''
        시그널 이벤트 등록
        '''
        pass

    def detach_signal(self):
        pass

    def get_signal_list(self):
        pass
