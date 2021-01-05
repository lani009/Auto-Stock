from PyQt5.QtWidgets import QApplication
import sys
from algorithms.impl.fifteen_candle import FifteenCandel
from dao.dao import Dao
from threads.index import Index
from threads.realtime.realtime import Realtime


def main():
    print("Auto Stock start")

    index_class = Index()
    index_class.__setattr__
    app = QApplication(sys.argv)
    app.exec_()


if __name__ == "__main__":
    main()
