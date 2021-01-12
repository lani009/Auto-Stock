from enum import Enum, auto


class OfferStock(Enum):
    BUYING = auto()
    SELLING = auto()


class CandleUnit(Enum):
    TICK = auto()
    SECOND = auto()
    MINUIT = auto()
    HOUR = auto()


class RealTimeDataEnum(Enum):
    CURRENT_PRICE = 10
    VOLUME = 15
    START_PRICE = 16
    HIGH_PRICE = 17
    LOW_PRICE = 18
    ACCUMULATED_VOLUME = 13
    MARKET_CAP = 311


class TrCode(Enum):
    OPT10080 = "주식분봉차트조회요청"
    OPT10001 = "주식기본정보요청"
