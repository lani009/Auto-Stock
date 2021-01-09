from request.enum.stockEnum import CandleUnit
import datetime
from entity.candle import Candle


class CandleChart():
    __unit: CandleUnit   # 봉 단위

    '''
    __cycle = 틱 사이즈
    ex)
    __unit = 분
    __cycle = 30
    30분봉
    '''
    __cycle: int    # 틱 단위

    __candle_list: list

    def __init__(self, unit: CandleUnit, cycle: int, candle_list):
        self.__unit = unit
        self.__cycle = cycle
        self.__candle_list = candle_list

    def get_cycle(self) -> int:
        return self.__cycle

    def get_unit(self) -> CandleUnit:
        '''
        봉 차트의 단위를 리턴
        '''
        return self.__unit

    def get_candle_list(self) -> list(Candle):
        '''
        캔들을 list 형태로 리턴
        '''
        return self.__candle_list

    def get_candle_by_index(self, index: int):
        '''
        index번 째의 캔들을 리턴
        '''
        return self.__candle_list[index]


class Candle():
    __volume: int                    # 거래량
    __start_price: int               # 시가
    __end_price: int                 # 종가
    __low_price: int                 # 저가
    __high_price: int                # 고가
    __exe_time: datetime.datetime    # 체결시간

    def __init__(self, volume: int, start_price: int, end_price: int, low_price: int, high_price: int, exe_time: datetime.datetime):
        self.__volume = volume
        self.__start_price = start_price
        self.__end_price = end_price
        self.__low_price = low_price
        self.__high_price = high_price
        self.__exe_time = exe_time

    def get_data(self):
        '''
        봉 하나에 대한 데이터를 불러온다
        return value
        ------------
        {
            "거래량": self.__volume,
            "시가": self.__start_price,
            "종가": self.__end_price,
            "저가": self.__low_price,
            "고가": self.__high_price,
            "체결시간": self.__exe_time
        }
        '''
        return {
            "거래량": self.__volume,
            "시가": self.__start_price,
            "종가": self.__end_price,
            "저가": self.__low_price,
            "고가": self.__high_price,
            "체결시간": self.__exe_time
        }
