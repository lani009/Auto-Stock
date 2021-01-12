from request.enum.stockEnum import CandleUnit
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

    def get_candle_list(self) -> [Candle, ...]:
        '''
        캔들을 list 형태로 리턴
        '''
        return self.__candle_list

    def get_candle_by_index(self, index: int) -> Candle:
        '''
        index번 째의 캔들을 리턴
        '''
        return self.__candle_list[index]