import copy
from typing import List
from AutoStock.entity.stock import Stock
from AutoStock.algorithms.algorithm import Algorithm


class AlgoritmRunner():
    '''
    알고리즘을 총괄해 주는 클래스
    '''
    __algorithm_list: List[Algorithm] = []

    def __init__(self):
        pass

    def stop_all(self):
        '''
        작동하고 있는 전체 알고리즘을 종료시킨다.
        '''
        for algorithm in self.__algorithm_list:
            algorithm.force_selling()   # 보유 주식 강제 매도
            algorithm.stop_algorithm_thread()   # 스레드 종료
            self.__algorithm_list.clear()

    def stop(self, algorithm_param: Algorithm):
        '''
        특정 알고리즘만 종료
        '''
        algorithm_found = next((algorithm for algorithm in self.__algorithm_list if algorithm == algorithm_param), None)

        if algorithm_found is None:
            raise RuntimeError("Algorithm이 정상적으로 주어지지 않았습니다.")

        algorithm_found.force_selling()
        algorithm_found.stop_algorithm_thread()
        self.__algorithm_list.remove(algorithm_found)

    def register_algorithm(self, algorithm: Algorithm, stock: Stock) -> None:
        '''
        해당 알고리즘이 작동할 수 있도록, 알고리즘 목록에 등록한다.
        '''
        algorithm_param = algorithm(stock)          # 알고리즘 객체 생성
        algorithm_param.start_algorithm_thread()    # 알고리즘 스레드 실행
        print("AUTO STOCK ALGORITHM Initiate")
        self.__algorithm_list.append(algorithm_param)  # 알고리즘 리스트에 추가

    def get_algorithm_list(self) -> List[Algorithm]:
        '''
        현재 작동하고 있는 알고리즘의 목록을 반환한다.
        '''
        return copy.deepcopy(self.__algorithm_list)
