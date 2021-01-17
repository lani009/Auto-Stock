from PyQt5.QtCore import Null, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5 import uic
from request.dao import Dao
from entity.stock import Stock


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
        


    def setupUI(self):
        self.program = uic.loadUi("./python/src/AutoStock/qtui/index.ui", self)
        
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
        
    
    @pyqtSlot()
    def show_bought_stock(self):
        '''
        구매한 종목 show
        '''
        stock = Dao().load_stock
        
        self.stockNameLabel.setText(stock.get_str_name)
    
    @pyqtSlot()
    def show_now_price(self):
        stock = Dao().load_stock()
        if stock != Null:

            price =

            self.priceLabel.setText(price)
        elif stock == Null:
            self.priceLabel.setText(" ")

    @pyqtSlot()
    def show_profit(self):
        profit=
        
        self.priceLabel.setText(profit)

    @pyqtSlot
    def show_candle_chart(self):









if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    
    app.exec()