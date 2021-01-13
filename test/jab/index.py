from ang import ang
from PyQt5.QtCore import QThread



class Index(QThread):
    '''
    주식 총괄 메인 클래스
    '''
    pass

    def __init__(self):
        self.ang = ang()

    def run(self):
        '''
        메인
        '''

        name = "15_pivot2"


        self.ang.condition_slot(name)
        print(name)
        code_list = self.ang.condition_tr_slot()
        print(code_list)
