class Dao():
    '''
    키움 API Data Access Object 클래스

    '''
    __request_queue = None

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            cls._init = True

    def request_data(self):
        pass

    def request_candle(self, stock: str, tick: int) -> list:
        pass

    def reg_slot(self, callback):
        pass
