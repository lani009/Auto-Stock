import sys
sys.path.append("./AutoStock")

from AutoStock.request.dao import Dao
from AutoStock.algorithms.impl.fifteen_bottom import FifteenBottom
from AutoStock.threads.algorithm_runner import AlgoritmRunner
from PyQt5.QtWidgets import QApplication


class MainRunner():
    __algorithm_runner: AlgoritmRunner = None
    __NINEOCLOCK = None
    def __init__(self):
        self.__algorithm_runner = AlgoritmRunner()
        Dao().login()
        Dao().set_chejan_data_callback(self.echo)
        Dao().set_server_msg_callback(self.echo)

    def run_program(self):
        filtered_stock_list = FifteenBottom.filter_list()
        for stock in filtered_stock_list:
            self.__algorithm_runner.register_algorithm(FifteenBottom, stock)

        return

    def echo(self, arg):
        print(arg)


if __name__ == "__main__":
    app = QApplication([])
    main_runner = MainRunner()
    main_runner.run_program()
    sys.exit(app.exec_())
