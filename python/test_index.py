import sys
from request.dao import Dao
import sys
from PyQt5.QtWidgets import QApplication
import unittest

sys.path.append("D:/git/Auto-Stock/python")


class AutoStockTest(unittest.TestCase):
    pass


class MainTest():
    def __init__():
        pass

    def main():
        Dao().login()
        data = Dao().request_candle_data()
        data.plot()


def main():
    print("Auto Stock Test start")

    app = QApplication(sys.argv)
    index_class = MainTest()
    index_class.main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
