import logging
import sys

from PyQt5.QtWidgets import QApplication

from AutoStock.algorithms.impl.fifteen_bottom import FifteenBottom
from AutoStock.request.dao import Dao
from AutoStock.threads.algorithm_runner import AlgoritmRunner


class MainRunner():
    __algorithm_runner: AlgoritmRunner = None
    __NINEOCLOCK = None

    def __init__(self):
        logging.basicConfig(filename="./autostock.log", filemode="w", level=logging.DEBUG)
        # logging.getLogger().addHandler(logging.StreamHandler())
        self.__algorithm_runner = AlgoritmRunner()
        Dao().login()
        Dao().set_chejan_data_callback(self.echo)
        Dao().set_server_msg_callback(self.echo)

    def run_program(self):
        filtered_stock_list = FifteenBottom.filter_list()
        if filtered_stock_list.__len__() == 0:
            raise RuntimeError("filter list 결과 없음.")
        for stock in filtered_stock_list:
            self.__algorithm_runner.register_algorithm(FifteenBottom, stock)


    def echo(self, arg):
        print(arg)


if __name__ == "__main__":
    app = QApplication([])
    main_runner = MainRunner()
    main_runner.run_program()
    sys.exit(app.exec_())
