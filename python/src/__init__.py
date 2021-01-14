from PyQt5.QtWidgets import QApplication
import sys
from threads.index import Index


def main():
    print("Auto Stock start")

    app = QApplication(sys.argv)
    index_class = Index()
    index_class.start()
    app.exec_()


if __name__ == "__main__":
    main()
