from pandas import Series, DataFrame
import queue

from request.enum.stockEnum import CandleUnit
from request.enum.stockEnum import TrCode
from entity.stock import Stock
from entity.candleChart import CandleChart
from request.kiwoom import Kiwoom
from datetime import datetime


class Dao():
    '''
    Signleton

    키움 API Data Access Object 클래스
    '''
    __request_queue = queue.Queue(maxsize=1)    # size를 1로 막아두어, 하나 이상의 요청이 들어올 경우 해당 스레드는 blocking 되게함
    __kiwoom_obj: Kiwoom
    __realtime_data_list = []     # 현재 reg 되어 있는 realtime data 들의 목록

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            self.__kiwoom_obj = Kiwoom()
            self.__kiwoom_obj.set_realtime_callback(self._realtime_data_processor)
            # TODO 로그인 작성
            cls._init = True

    def login(self):
        self.__kiwoom_obj.do_login()



    def request_tr_data(self, input_value: dict, trEnum: TrCode, nPrevNext: int, sScreenNo: str):
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
        self.__request_queue.put(0)
        data = self.__kiwoom_obj.get_tr_data(input_value, trEnum, nPrevNext, sScreenNo)
        self.__request_queue.get()
        return data

    def request_candle_data(self, stock: Stock, unit: CandleUnit, tick: int) -> CandleChart:
        '''
        키움 서버에 봉 차트 데이터를 요청한다.

        param
        ------
        unit: 봉 단위

        tick: 틱 단위
        '''
        self.__request_queue.put(0)

        data = None
        if unit == CandleUnit.DAY:
            today_date = self.get_today_date()
            data = self.__kiwoom_obj.get_tr_data({
                "종목코드": stock.get_int_name,
                "기준일자:": today_date,
                "수정주가구분": 0
            }, TrCode.OPT10081, 0, 2000, [], ["체결시간", "시가", "현재가", "저가", "고가", "거래량"])

        elif unit == CandleUnit.MINUIT:
            data = self.__kiwoom_obj.get_tr_data({
                "종목코드": stock.get_int_name,
                "틱범위:": tick,
                "수정주가구분": 0
            }, TrCode.OPT10080, 0, 2000, [], ["체결시간", "시가", "현재가", "저가", "고가", "거래량"])

        elif unit == CandleUnit.TICK:
            data = self.__kiwoom_obj.get_tr_data({
                "종목코드": stock.get_int_name,
                "틱범위:": tick,
                "수정주가구분": 0
            }, TrCode.OPT10079, 0, 2000, [], ["체결시간", "시가", "현재가", "저가", "고가", "거래량"])

        time_list = [m_data["체결시간"] for m_data in data["multi_data"]]
        open_list = [m_data["시가"] for m_data in data["multi_data"]]
        close_list = [m_data["현재가"] for m_data in data["multi_data"]]
        low_list = [m_data["저가"] for m_data in data["multi_data"]]
        high_list = [m_data["고가"] for m_data in data["multi_data"]]
        volume_list = [m_data["거래량"] for m_data in data["multi_data"]]
        dict_data = {"time": time_list, "open": open_list, "close": close_list, "low": low_list, "high": high_list, "volume": volume_list}
        prc_data = DataFrame(dict_data)

        ma5 = (prc_data.close.rolling(5).mean())
        ma10 = (prc_data.close.rolling(10).mean())
        ma20 = (prc_data.close.rolling(20).mean())
        ma60 = (prc_data.close.rolling(60).mean())

        prc_data.insert(len(prc_data.columns), "ma5", ma5)
        prc_data.insert(len(prc_data.columns), "ma10", ma10)
        prc_data.insert(len(prc_data.columns), "ma20", ma20)
        prc_data.insert(len(prc_data.columns), "ma60", ma60)

        return prc_data

    def request_SMA_data(self):
        # candle = self.request_candle_data()
        # 캔들 최근 종가 1~5까지의 합/5
        # 캔들 최근 종가 1~10까지의 합/10
        # 캔들 최근 종가 1~20까지의 합/20
        '''
        이동평균 데이터
            1분전 2분전 3분전 4분전 5분전
        5
        10
        20
        '''
        pass

    def reg_realtime_data(self, callback, stock: Stock, realtimeDataList):
        '''
        해당 주식의 실시간 데이터 처리 콜백을 등록한다.
        '''
        self.__request_queue.put(0)
        self.__realtime_data_list.append([callback, realtimeDataList, stock])     # 실시간 데이터 처리 목록에 추가
        self.__kiwoom_obj.set_realtime_reg(2000, [stock], realtimeDataList)
        self.__request_queue.get()

    def request_condition_list(self):
        '''
        조건식 목록을 반환한다.

        return
        -------
        [
            [인덱스 번호, 조건식 이름],
            [인덱스 번호, 조건식 이름],
            ...
        ]
        '''
        return self.__kiwoom_obj.get_condition_list()

    def request_stock_instance(self, stock_code):
        '''
        종목 코드에 해당하는 Stock 객체를 반환한다.
        '''
        tr_data = self.__kiwoom_obj.get_tr_data({"종목코드": stock_code}, TrCode.OPT10001,
                                                0, 2000, ["종목명", "PER", "PBR"], [])

        stock_temp = Stock(tr_data["single_data"]["종목명"], stock_code)
        stock_temp.set_per(float(tr_data["single_data"]["PER"]))
        stock_temp.set_pbr(float(tr_data["single_data"]["PBR"]))
        return stock_temp

    def request_condition_stock(self, index, cond_name):
        '''
        해당 조건식에 부합하는 주식 종목을 반환한다.

        param
        ------
        index: 조건식 인덱스 번호

        cond_name: 조건식 이름

        return
        -------
        [Stock, Stock, ...]
        Stock 객체를 list로 wrapping하여 반환한다.
        '''
        stock_code_list = self.__kiwoom_obj.get_condition_stock(2000, index, cond_name)

        stock_list = []     # Stock 객체 리스트
        for stock_code in stock_code_list:
            stock_list.append(self.request_stock_instance(stock_code))

        return stock_list

    def _realtime_data_processor(self, sCode, sRealType, sRealData):
        stock = self.request_stock_instance(sCode)
        for realtime_list in self.__realtime_data_list:
            if realtime_list[1] == stock:
                realtime_list[0]()

    def get_today_date():
        '''
        당일의 날짜를 yyyymmdd로 반환한다.
        일봉 조회에서 사용됨.
        '''
        date_today = datetime.today()
        return date_today.strftime('20%y%m%d')

    def request_user_ma(data: DataFrame, number1: int, ma1: int, number2: int, ma2: int):
        '''
         사용자 지정
         이동평균선의 '1봉전' 지표를 생성하여 데이터프레임에 추가 후 반환
         number1, number2 -> 이평선과의 괴리 정도
         ma1, ma2 -> 이평선 기간
        '''

        user_ma1 = data["close"].rolling(ma1).mean() * number1
        data.insert(len(data.columns), "user_ma1", user_ma1)

        user_ma2 = data["close"].rolling(ma2).mean() * number2
        data.insert(len(data.columns), "user_ma2", user_ma2)

        data["user_ma1"] = data["user_ma1"].shift(1)
        data["user_ma2"] = data["user_ma2"].shift(1)

        return data
