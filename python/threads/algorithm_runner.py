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
        pass

    def stop(self):
        '''
        특정 알고리즘만 종료
        '''
        pass

    def register_algorithm(self, algorithm: Algorithm, stock: Stock):
        algorithm_param = algorithm(stock)
        self.__algorithm_list.append(algorithm_param)

    def get_algorithm_list(self):
        pass
