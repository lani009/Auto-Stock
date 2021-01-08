import queue
from request.enum.stockEnum import CandleUnit
from entity.stock import Stock
from entity.candle import CandleChart
from request.kiwoom import Kiwoom


class Dao():
    '''
    키움 API Data Access Object 클래스

    '''
    __request_queue = queue.Queue(maxsize=1)
    __kiwoom_obj: Kiwoom

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            self.__kiwoom_obj = Kiwoom()
            # TODO 로그인 작성
            cls._init = True

    def request_tr_data(self, input_value: dict, sRQName: str, sTrCode: str, nPrevNext: int, sScreenNo: str):
        '''
        키움 서버에 tr 데이터를 요청한다.

        input_value
        -----------
        input_value는 SetInputValue에 들어갈 내용이다.
        dictionary 타입이다.

        ex)
        input_value = {
            "시장구분": "입력값 1",
            "주가구분": "입력값 2",
            "거래량구분": "입력값 3
        }

        SetInputValue("시장구분", "입력값 1");

        SetInputValue("주기구분", "입력값 2");

        SetInputValue("거래량구분", "입력값 3");
        '''
        self.__request_queue.put([input_value, sRQName, sTrCode, nPrevNext, sScreenNo])
        self.__kiwoom_obj.get_tr_data(input_value, sRQName, sTrCode, nPrevNext, sScreenNo)
        self.__request_queue.get()
        pass

    def request_candle_data(self, stock: Stock, unit: CandleUnit, tick: int) -> CandleChart:
        '''
        키움 서버에 봉 차트 데이터를 요청한다.

        param
        ------
        unit: 봉 단위

        tick: 틱 단위
        '''
        self.__request_queue.put([stock, unit, tick])
        pass

    def reg_slot(self, callback, stock: Stock):
        '''
        해당 주식의 실시간 데이터 슬롯을 등록한다.
        '''
        self.__request_queue.put()
        pass
