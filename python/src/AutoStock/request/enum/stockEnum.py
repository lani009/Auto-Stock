from enum import Enum, auto, unique


class OfferStock(Enum):
    BUYING = auto()
    SELLING = auto()


class CandleUnit(Enum):
    TICK = auto()
    SECOND = auto()
    MINUTE = auto()
    HOUR = auto()
    DAY = auto()


@unique
class RealTimeDataEnum(Enum):
    CURRENT_PRICE = 10  # 현재가
    VOLUME = 15  # 거래량
    OPEN_PRICE = 16  # 시가
    HIGH_PRICE = 17  # 고가
    LOW_PRICE = 18  # 저가
    ACCUMULATED_VOLUME = 13 # 누적 거래량
    MARKET_CAP = 311    # 시가총액


class TrCode(Enum):
    OPT10079 = "주식틱차트조회요청"
    OPT10080 = "주식분봉차트조회요청"
    OPT10081 = "주식일봉차트조회요청"
    OPT10001 = "주식기본정보요청"
