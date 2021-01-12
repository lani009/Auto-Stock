import datetime


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
