from PyQt5.QtCore import QThread

from threads.algorithm_runner import AlgoritmRunner
from algorithms.impl.fifteen_candle import FifteenCandel

import time


class Index(QThread):
    '''
    주식 총괄 메인 클래스
    '''
    pass

    def __init__(self):
        self.algorithm_runner = AlgoritmRunner()

    def run(self):
        '''
        메인
        '''
        current_time = time.time()

        if current_time > "9시 25분":
            selected_stock = FifteenCandel.filter_list()

            for stock in selected_stock:
                # 알고리즘이 돌아가도록 등록
                self.algorithm_runner.register_algorithm(FifteenCandel, stock)
