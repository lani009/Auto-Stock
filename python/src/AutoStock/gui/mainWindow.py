from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5 import uic




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
        


    def setupUI(self):
        self.form_class = uic.loadUi("./python/src/AutoStock/qtui/index.ui", self)
        
        self.setWindowTitle("tenok")
        self.show()
        

    @pyqtSlot()
    def sellingBtn_clicked(self):
        '''
        버튼 클릭시 전체 매도
        
        '''
        print("매도")

    @pyqtSlot()
    def stopBtn_clicked(self):
        '''
        버튼 클릭시 프로그램 중지
        '''
        print("중지")
    











if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    
    app.exec()