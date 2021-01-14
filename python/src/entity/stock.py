class Stock():
    '''
    엔티티 클래스
    =========
    주식에서 하나의 '종목'에 대한 클래스이다.
    '''
    __stock_name_by_str = None    # string 타입 종목 이름
    __stock_name_by_code = None    # 숫자 타입 종목 코드
    __per = 0.0
    __pbr = 0.0

    def __init__(self, str_name: str, code_name: int):
        '''
        str_name: 종목 이름

        code_name: 종목 코드
        '''
        self.__stock_name_by_str = str_name
        self.__stock_name_by_code = code_name

    def __eq__(self, obj):
        return self.__stock_name_by_code == obj.__stock_name_by_code

    def get_str_name(self):
        '''
        종목 이름 반환
        '''
        return self.__stock_name_by_str

    def get_code_name(self):
        '''
        종목 코드 반환
        '''
        return self.__stock_name_by_int

    def get_per(self):
        return self.__per

    def get_pbr(self):
        return self.__pbr

    def set_per(self, per):
        if type(per) is not float:
            raise TypeError("parameter per is not float")
        self.__per = per

    def set_pbr(self, pbr):
        if type(pbr) is not float:
            raise TypeError("parameter pbr is not float")
        self.__pbr = pbr
