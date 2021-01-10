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
