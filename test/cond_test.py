from PyQt5.QtCore import QEventLoop
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtWidgets import QApplication
import sys


class Main():
    __kiwoom = None
    __event_loop = None
    __condition_list = []
    __condition_stock_list = []

    def __init__(self):
        self.__kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.__event_loop = QEventLoop()

        self.__kiwoom.OnEventConnect.connect(self.__login_slot)
        self.__kiwoom.OnReceiveConditionVer.connect(self.__condition_ver_slot)
        self.__kiwoom.OnReceiveTrCondition.connect(self.__send_condition_slot)

    def login(self):
        self.__kiwoom.dynamicCall("CommConnect()")
        self.__event_loop.exec_()

    def get_condition_list(self):
        self.__kiwoom.dynamicCall("GetConditionLoad()")
        self.__event_loop.exec_()
        return self.__condition_list

    def print_condition_list(self, cond):
        self.__kiwoom.dynamicCall("SendCondition(QString, QString, int, int)", "2000", cond[1], cond[0], 0)
        self.__event_loop.exec_()

        print("{} 조건식의 검색 결과".format(cond[1]))
        i = 1
        for stock in self.__condition_stock_list:
            print("{} ".format(stock), end="")
            if i % 10 == 0:
                print()
            i += 1

    def __condition_ver_slot(self, lRet, sMsg):
        condition_name_list: str
        condition_name_list = self.__kiwoom.dynamicCall("GetConditionNameList()")
        '''
        condition_name_list
        ==============
        인덱스^조건식이름;인덱스^조건식이름;
        '''

        for cond_index_name in condition_name_list[:-1].split(";"):
            self.__condition_list.append(cond_index_name.split("^"))

        self.__event_loop.exit()

    def __login_slot(self, errNo):
        self.__event_loop.exit()

    def __send_condition_slot(self, sScrNo, strCodeList, strConditionName, nIndex, nNext):
        self.__condition_stock_list = strCodeList.split(";")
        self.__event_loop.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.login()
    condition_list = main.get_condition_list()

    print(condition_list)

    main.print_condition_list(condition_list[1])
    sys.exit(app.exit())
