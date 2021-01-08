class CandleChart():
    __unit = "S"    # 캔들 단위

    '''
    __cycle = 틱 사이즈
    ex)
    __unit = 분
    __cycle = 30
    30분봉
    '''
    __cycle = 1

    def __init__(self):
        pass

    def get_cycle(self):
        return self.__cycle

    def get_unit(self):
        pass


class Candle():
    pass
