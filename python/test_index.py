import sys
sys.path.append("D:/git/Auto-Stock/python")
from request.dao import Dao
from PyQt5.QtWidgets import QApplication
import unittest



class AutoStockTest(unittest.TestCase):
    pass


class MainTest():
    def __init__(self):
        pass

    def main(self):
        Dao().login()
        data = Dao().request_candle_data_from_now()
        data.plot()


def main():
    print("Auto Stock Test start")

    app = QApplication(sys.argv)
    index_class = MainTest()
    index_class.main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
