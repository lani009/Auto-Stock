from PyQt5.QtWidgets import QApplication
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop
import sys
from ang import ang
from controller import controller


class Main():
    def __init__(self):
        print("Main() start")

        self.app = QApplication(sys.argv)
        kiwoom = controller()
        kiwoom.run()
        self.app.exec_()
        print("hi")


if __name__ == "__main__":
    Main()
