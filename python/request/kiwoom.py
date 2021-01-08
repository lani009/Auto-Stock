from PyQt5.QAxContainer import QAxWidget


class Kiwoom(QAxWidget):
    '''
    키움 통신 클래스
    =============
    키움 API와 직접적인 통신을 진행한다.

    Thread_safe함.

    TODO
    -----------
    이벤트루프를 적용하여 get_tr_data 등의 메소드가 thread safe 해야함
    '''

    def __init__(self):
        pass

    def get_tr_data(self):
        pass


"""
tr data
opt10001 주식기본정보요청 -> 종목코드/ 종목명
opt10080 주식분봉차트조회요청 -> 거래량 / 시가 / 고가 / 저가


Real Type
주식 시세 -> 10 현재가/ 12 등락율 / 16 시가 / 17 고가/ 18 저가
주식 호가 잔량 -> 121 매도호가총잔량 / 125 매수호가총잔량
"""
