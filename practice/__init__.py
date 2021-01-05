import sys
from kiwoom.kiwoom import Kiwoom
from PyQt5.QtWidgets import QApplication


class Main():
    def __init__(self):
        print("Main() start")

        self.app = QApplication(sys.argv)
        self.kiwoom = Kiwoom()
        self.app.exec_()
        print("hi")


if __name__ == "__main__":
    Main()
