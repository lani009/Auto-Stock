from entity.stock import Stock
from algorithms.algorithm import Algorithm


class AlgoritmRunner():
    '''
    알고리즘을 총괄해 주는 클래스
    '''
    __algorithm_list = []

    def __init__(self):
        pass

    def stop_all(self):
        '''
        작동하고 있는 전체 알고리즘을 종료시킨다.
        '''
        pass

    def stop(self, algorithm: Algorithm):
        '''
        특정 알고리즘만 종료
        '''
        pass

    def register_algorithm(self, algorithm: Algorithm, stock: Stock) -> None:
        '''
        해당 알고리즘이 작동할 수 있도록, 알고리즘 목록에 등록한다.
        '''
        algorithm_param = algorithm()        # 알고리즘 객체 생성
        self.__algorithm_list.append(algorithm_param)  # 알고리즘 리스트에 추가

    def get_algorithm_list(self) -> list:
        '''
        현재 작동하고 있는 알고리즘의 목록을 반환한다.
        '''
        return self.__algorithm_list
