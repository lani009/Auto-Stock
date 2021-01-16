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
    SEND_ORDER = "주식주문요청"

class TrClassification(Enum):
    LIMIT = "00"    # 지정가
    MARKET = "03"   # 시장가

    COND_LIMIT = "05"   # 조건부 지정가
    BEST_LIMIT = "06"   # 최유리 지정가
    FP_LIMIT = "07"     # 최우선 지정가

    LIMIT_IOC = "10"    # 지정가 IOC
    MARKET_IOC = "13"   # 시장가 IOC
    BEST_IOC = "16"     # 최유리 IOC

    LIMIT_FOK = "20"    # 지정가 FOK
    MARKET_FOK = "23"   # 시장가 FOK
    BEST_FOK = "26"     # 최유리 FOK

    PRE_REGULAR = "61"  # 장전 시간외
    SINGLE_AUCTION = "62"   # 시간외 단일가
    POST_REGULAR = "81"     # 장후 시간외
