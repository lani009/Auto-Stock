class Stock():
    '''
    엔티티 클래스
    =========
    주식에서 하나의 '종목'에 대한 클래스이다.
    '''
    __stock_name_by_str: str    # string 타입 종목 이름
    __stock_name_by_int: int    # int 타입 종목 코드

    def __init__(self, str_name: str, int_name: int):
        '''
        str_name: 종목 이름

        int_name: 종목 코드
        '''
        self.__stock_name_by_str = str_name
        self.__stock_name_by_int = int_name

    def get_str_name(self):
        '''
        종목 이름 반환
        '''
        return self.__stock_name_by_str

    def get_int_name(self):
        '''
        종목 코드 반환
        '''
        return self.__stock_name_by_int
