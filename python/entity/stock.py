from entity.candle import Candle
from entity.candle import CandleChart


class Stock():
    '''
    엔티티 클래스
    =========
    주식에서 하나의 '종목'에 대한 클래스이다.
    '''
    __stock_name_by_str: str    # string 타입 종목 이름
    __stock_name_by_int: int    # int 타입 종목 코드

    def __init__(self):
        pass

    def get_current_data(self):
        pass

    def get_candle(self, tick: int) -> CandleChart:
        '''
        봉 차트를 CandleChart 형태로 반환한다.

        attribute
        ---------
        tick: 틱
        '''
        pass
