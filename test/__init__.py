from PyQt5.QtWidgets import QApplication
import sys
from index import Index


class Main():
    def __init__(self):
        print("Main() start")

        self.app = QApplication(sys.argv)
        kiwoom = Index()
        kiwoom.run()
        self.app.exec_()
        print("hi")


if __name__ == "__main__":
    Main()
