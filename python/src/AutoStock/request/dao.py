import concurrent.futures
import queue
import time
from datetime import datetime
from typing import Callable, Dict, List, Tuple, Union

from AutoStock.entity.stock import Stock
from pandas import DataFrame

from AutoStock.request.enum.stockEnum import (CandleUnit, OrderType, RealTimeDataEnum,
                                    TrClassification, TrCode)
from AutoStock.request.kiwoom import Kiwoom


class Dao():
    '''
    Signleton

    키움 API Data Access Object 클래스
    '''
    __request_queue = queue.Queue(maxsize=10)    # size를 1로 막아두어, 하나 이상의 요청이 들어올 경우 해당 스레드는 blocking 되게함
    __kiwoom_obj: Kiwoom
    __realtime_data_list: List[Tuple[Callable, List[RealTimeDataEnum], Stock]]     # 현재 reg 되어 있는 realtime data 들의 목록
    __thread_executor = concurrent.futures.ThreadPoolExecutor(max_workers=30)   # 실시간 데이터 Condition 검증 처리용 스레드풀
    __server_msg_callback: Callable = None
    __chejan_data_callback: Callable = None
    __buying_price_dict: Dict[Stock, int] = {}
    __accno: str = None     # 계좌번호
    __bought_stock_list: List[Tuple[Stock, int, int]] = None    # 매수한 주식 목록. [주식, 가격, 주수]
    # __buying_stock: Stock = None

    def __new__(cls, *_, **__):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            self.__kiwoom_obj = Kiwoom()
            self.__realtime_data_list = []
            self.__kiwoom_obj.set_realtime_callback(self._realtime_data_processor)
            self.__kiwoom_obj.set_server_msg_callback(self._server_msg_callback_processor)
            cls._init = True

    def login(self):
        self.__kiwoom_obj.do_login()

    def request_tr_data(self, input_value: dict, trEnum: TrCode, nPrevNext: int, sScreenNo: str,
                        rqSingleData: Dict[str, str], rqMultiData: Dict[str, str]):
        '''
        키움 서버에 tr 데이터를 요청한다.

        Args:
            input_value: 하단 참조.

            trEnum: TrCode 타입

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
        data = self.__kiwoom_obj.get_tr_data(input_value, trEnum, nPrevNext, sScreenNo, rqSingleData, rqMultiData)
        self.__request_queue.get()
        return data

    def request_candle_data(self, stock, unit, tick: int) -> DataFrame:
        '''캔들 데이터 불러오는 메소드

        Parameters
        ----------
        stock :
            검색 대상 주식 인스턴스

        unit :
            봉 단위

        tick :
            틱 단위

        Returns
        -------
        DataFrame
            캔들 데이터
        '''
        raise NotImplementedError()

    def request_candle_data_from_now(self, stock: Stock, unit: CandleUnit, tick: int) -> DataFrame:
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
            data = self.__kiwoom_obj.get_tr_data({
                "종목코드": stock.get_code_name(),
                "기준일자": tick,
                "수정주가구분": 0
            }, TrCode.OPT10081, 0, 2000, [], ["일자", "시가", "현재가", "저가", "고가", "거래량"])

        elif unit == CandleUnit.MINUTE:
            data = self.__kiwoom_obj.get_tr_data({
                "종목코드": stock.get_code_name(),
                "틱범위": tick,
                "수정주가구분": 0
            }, TrCode.OPT10080, 0, 2000, [], ["체결시간", "시가", "현재가", "저가", "고가", "거래량"])

        elif unit == CandleUnit.TICK:
            data = self.__kiwoom_obj.get_tr_data({
                "종목코드": stock.get_code_name(),
                "틱범위": tick,
                "수정주가구분": 0
            }, TrCode.OPT10079, 0, 2000, [], ["체결시간", "시가", "현재가", "저가", "고가", "거래량"])

        if unit == CandleUnit.MINUTE or unit == CandleUnit.TICK:

            time_list = [m_data["체결시간"] for m_data in data["multi_data"]]
        else:
            time_list = [m_data["일자"] for m_data in data["multi_data"]]

        open_list = [abs(int(m_data["시가"])) for m_data in data["multi_data"]]      # 시가
        close_list = [abs(int(m_data["현재가"])) for m_data in data["multi_data"]]   # 종가
        low_list = [abs(int(m_data["저가"])) for m_data in data["multi_data"]]      # 저가
        high_list = [abs(int(m_data["고가"])) for m_data in data["multi_data"]]     # 고가
        volume_list = [int(m_data["거래량"]) for m_data in data["multi_data"]]      # 거래량

        date_time_list = []  # datetime 객체 저장용 -> str to datetime

        if unit == CandleUnit.MINUTE or unit == CandleUnit.TICK:
            for time_str in time_list:
                date_time = datetime.strptime(time_str.replace(" ", ""), "%Y%m%d%H%M%S")
                date_time_list.append(date_time)
        else:
            for time_str in time_list:
                date_time = datetime.strptime(time_str.replace(" ", ""), "%Y%m%d")
                date_time_list.append(date_time)

        dict_data = {"time": date_time_list, "open": open_list, "close": close_list, "low": low_list, "high": high_list, "volume": volume_list}
        prc_data = DataFrame(dict_data)
        prc_data['percentage'] = ((prc_data.close - prc_data.open) / prc_data.open * 100)

        prc_data.insert(len(prc_data.columns), "ma5", prc_data.close.rolling(5).mean())
        prc_data.insert(len(prc_data.columns), "ma10", prc_data.close.rolling(10).mean())
        prc_data.insert(len(prc_data.columns), "ma20", prc_data.close.rolling(20).mean())
        prc_data.insert(len(prc_data.columns), "ma60", prc_data.close.rolling(60).mean())

        self.__request_queue.get(0)

        return prc_data

    def reg_realtime_data(self, callback: Callable, stock: Stock, realtimeDataList: List[RealTimeDataEnum]):
        '''
        해당 주식의 실시간 데이터 처리 콜백을 등록한다.

        Parameter
        ---------
        callback: realtime 이벤트가 발생했을 때, 호출될 콜백

        stock: 대상 주식

        realtimeDataList: 필요로 하는 실시간 데이터 목록
        '''
        self.__request_queue.put(0)
        self.__realtime_data_list.append((callback, realtimeDataList, stock))     # 실시간 데이터 처리 목록에 추가
        self.__kiwoom_obj.set_realtime_reg(2000, [stock.get_code_name()], realtimeDataList)
        self.__request_queue.get()

    def request_condition_list(self) -> List[Tuple[str, str]]:
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

    def request_stock_instance(self, stock_code: str) -> Stock:
        '''
        종목 코드에 해당하는 Stock 객체를 반환한다.

        Param
        ---------
        stock_code: 종목 코드
        '''
        self.__request_queue.put(0)
        tr_data = self.__kiwoom_obj.get_tr_data({"종목코드": stock_code}, TrCode.OPT10001,
                                                0, 3000, ["종목명", "PER", "PBR"], [])
        stock_obj = Stock(tr_data["single_data"]["종목명"], stock_code)

        if not tr_data["single_data"]["PER"]:
            # PER이 없을 경우
            stock_obj.set_per(0.0)
        else:
            stock_obj.set_per(float(tr_data["single_data"]["PER"]))

        if not tr_data["single_data"]["PBR"]:
            # PBR이 없을 경우
            stock_obj.set_pbr(0.0)
        else:
            stock_obj.set_pbr(float(tr_data["single_data"]["PBR"]))

        self.__request_queue.get()
        return stock_obj

    def request_condition_stock(self, index: Union[int, str], cond_name: str) -> List[Stock]:
        '''
        1초에 5개 정도의 주식만 불러올 수 있으니 주의!!!!!
        =================

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
        self.__request_queue.put(0)
        stock_code_list = self.__kiwoom_obj.get_condition_stock("3000", cond_name, index)   # 종목 코드 리스트
        print(stock_code_list)

        stock_list = []     # Stock 객체 리스트

        for stock_code in stock_code_list:
            self.__request_queue.get()
            stock_list.append(self.request_stock_instance(stock_code))
            self.__request_queue.put(0)
            time.sleep(1.7)   # QoS 안걸리는 최적의 숫자!

        self.__request_queue.get()
        return stock_list

    def buy_stock(self, stock: Stock, money: int):
        '''매수

        Parameters
        ----------
        stock :
            거래 대상 주식 인스턴스

        money :
            금액
        '''
        stock_current_price = self.__kiwoom_obj.get_tr_data({
            "종목코드": stock.get_code_name()
        }, TrCode.OPT10001, 0, 2000, ["현재가"], [])["현재가"]
        stock_n = stock_current_price // money     # 구매 예정 주 수
        self.__kiwoom_obj.send_order(2000, self.__accno, OrderType.BUY, stock.get_code_name(),
                                     stock_n, 0, TrClassification.BEST_FOK, 0)

        self.__bought_stock_list.append((stock, stock_current_price, stock_n))

    def sell_stock(self, stock: Stock):
        '''전액 매도

        Parameters
        ----------
        stock
        '''
        stock_found = next((list for list in self.__bought_stock_list if stock == list[0]), None)
        if stock_found is None:
            raise RuntimeError("해당 주식을 매수한 적이 없음.")

        self.__kiwoom_obj.send_order(2000, self.__accno, OrderType.SELL, stock.get_code_name(),
                                     stock_found[2], 0, TrClassification.BEST_FOK, 0)

    def set_buying_price(self, stock, price: int):
        '''매수 할 가격

        Parameters
        ----------
        stock :
        price :
        '''
        self.__buying_price_dict.setdefault(stock, price)

    def request_buying_price(self, stock):
        '''
        주식의 매수가격을 불러오는 메소드
        '''
        return self.__buying_price_dict.get(stock)

    # def store_stock(self, stock):
    #     '''
    #     매수한 주식을 저장하는 메소드
    #     '''
    #     self.__buying_stock = stock

    # def load_stock(self) -> Stock:
    #     '''
    #     매수한 주식을 불러오는 메소드
    #     '''
    #     return self.__buying_stock

    # def delete_stock(self):
    #     '''
    #     매도후 초기화
    #     '''
    #     self.__buying_stock = None

    def request_user_ma(self, data: DataFrame, number1: int, ma1: int, number2: int, ma2: int) -> DataFrame:
        '''
        사용자 지정
        이동평균선의 '1봉전' 지표를 생성하여 데이터프레임에 추가 후 반환

        param
        ----------
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

    
    def get_today_date(self) -> str:
        '''
        당일의 날짜를 yyyymmdd로 반환한다.

        일봉 조회에서 사용됨.
        '''
        return datetime.today().strftime('%Y%m%d')

    def set_server_msg_callback(self, callback: Callable):
        self.__server_msg_callback = callback

    def set_chejan_data_callback(self, callback: Callable):
        self.__chejan_data_callback = callback

    def _server_msg_callback_processor(self, data):
        self.__server_msg_callback(data)

    def _chejan_data_callback_processor(self, data):
        self.__chejan_data_callback(data)

    def _realtime_data_processor(self, sCode: str, _sRealType, _sRealData):
        stock = self.request_stock_instance(sCode)
        for realtime_list in self.__realtime_data_list:
            if realtime_list[2] == stock:
                realtime_data = self.__kiwoom_obj.parse_realtime(sCode, realtime_list[1])
                self.__thread_executor.submit(realtime_list[0], realtime_data)     # 스레드 풀을 통해 콜백 함수 호출
                break
