from typing import Any, Callable, Dict, List, Tuple
from request.enum.stockEnum import RealTimeDataEnum, TrCode, TrClassification
from request.enum.errCode import ErrCode
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop


class Kiwoom(QAxWidget):
    '''
    키움 통신 클래스
    =============
    키움 API와 직접적인 통신을 진행한다.

    Thread_safe함.

    TODO
    -----------
    이벤트루프를 적용하여 get_tr_data 등의 메소드가 thread safe 해야함
    '''

    __global_eventloop: QEventLoop = None               # 동기처리를 위한 전역 EventLoop
    __tr_data_temp: Dict[str, Dict[str, str]] = None    # GetTrData의 결과가 임시적으로 담기는 곳
    __condition_name_list: List[Tuple[str, str]] = None        # 조건식 이름과 인덱스가 임시적으로 담기는 곳
    __condition_stock_list: List[str] = None            # 조건식 필터링 결과가 임시적으로 담기는 곳
    __tr_rq_single_data: Dict[str, str] = None          # 사용자 요청 싱글데이터
    __tr_rq_multi_data: Dict[str, str] = None           # 사용자 요청 멀티데이터
    __realtime_data_callback: Callable = None           # 실시간 데이터 콜백
    __server_msg_callback: Callable = None
    __chejan_data_callback: Callable = None

    def __init__(self):
        super().__init__()
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        self.__global_eventloop = QEventLoop()
        self.__reg_all_slot()     # 이벤트 슬롯 등록

    def do_login(self):
        self.dynamicCall("CommConnect()")
        self.__global_eventloop.exec_()

    def get_tr_data(self, inputValue: Dict[str, str], trEnum: TrCode, nPrevNext: int, sScrNo: str,
                    rqSingleData: Dict[str, str], rqMultiData: Dict[str, str]):
        '''키움 API서버에 TR 데이터를 요청한다.

        Parameters
        ----------
        inputValue :
            KOA Studio 기준으로, SetInputValue에 들어갈 값

        trEnum : TrCode
            KOA Studio 기준, Tr 코드

        nPrevNext :
            prevNext

        sScrNo :
            스크린 번호

        rqSingleData :
            받아오고자 하는 싱글데이터 목록

        rqMultiData :
            받아오고자 하는 멀티데이터 목록

        Returns
        -------
        Dict[str, Dict[str, str]]
        '''
        self.__tr_rq_single_data = rqSingleData
        self.__tr_rq_multi_data = rqMultiData

        self._set_input_values(inputValue)   # inputvalue 대입
        r_value = self.dynamicCall("CommRqData(Qstring, QString, int, QString)",
                         trEnum.value, trEnum.name, nPrevNext, sScrNo)

        print(ErrCode(r_value))     # dynamic call 반환 값 출력
        self.__global_eventloop.exec_()
        return self.__tr_data_temp

    def get_condition_list(self):
        '''키움 증권 HTS에 저장되어 있는 조건식 목록들을 반환

        Returns
        -------
        (index, name)의 리스트를 반환한다.
        '''
        r_value = self.dynamicCall("GetConditionLoad()")
        print(ErrCode(r_value))     # dynamic call 반환 값 출력
        self.__global_eventloop.exec_()
        return self.__condition_name_list

    def get_condition_stock(self, sScrNo: str, cond_name: str, index: str) -> List[str]:
        '''
        해당 조건식을 만족하는 종목 코드를 리스트 형태로 반환

        Parameters
        ----------
        sScrNo : 스크린번호

        cond_name : 조건식 이름

        index : 조건식 인덱스 번호

        Returns
        -------
        Stock 객체들의 리스트를 반환한다.
        '''
        r_value = self.dynamicCall("SendCondition(QString, QString, int, int)", sScrNo, cond_name, index, 0)
        print(ErrCode(r_value))     # dynamic call 반환 값 출력
        self.__global_eventloop.exec_()
        return self.__condition_stock_list

    def set_realtime_reg(self, sScrNo: str, stockList: List[str], realtimeDataList: List[RealTimeDataEnum]):
        '''
        realtime data를 받아올 수 있도록 레지스터링 한다.

        Parameters
        ----------
        stockList : Stock 객체가 list 형태로 들어와야함

        realTimeDataList : RealTimeDataEnum 객체가 list 형태로 들어와야함
        '''
        if self.__realtime_data_callback is None:
            raise RuntimeError("realtime data callback 함수가 설정되지 않았습니다.")

        fid_list = "".join("{};".format(fid.value) for fid in realtimeDataList)[:-1]  # fid str list
        stock_code_list = "".join("{};".format(stock) for stock in stockList)[:-1]  # stock code str list

        r_value = self.dynamicCall("SetRealReg(QString, QString, QString, QString)", sScrNo, stock_code_list,
                                    fid_list, 1)
        print(ErrCode(r_value))

    def set_realtime_callback(self, callback: Callable):
        '''
        realtime data 이벤트가 발생했을 때, 이를 받아들일 콜백을 설정한다.
        '''
        self.__realtime_data_callback = callback

    def set_server_msg_callback(self, callback: Callable):
        '''서버로 부터 메시지가 도착했을 때, 이를 출력할 콜백을 설정한다.
        '''
        self.__server_msg_callback = callback

    def set_chejan_data_callback(self, callback: Callable):
        self.__chejan_data_callback = callback

    def send_order(self, sScrNo: str, sAccNo: str, nOrderType: TrClassification, sCode: str, nQty: int,
                   nPrice: int, sHogaGb, sOrgOrderNo: str):
        '''주식 주문

        Parameters
        ----------
        sScrNo :
            스크린번호

        sAccNo :
            계좌번호

        nOrderType :
            주문 유형

        sCode :
            종목코드

        nQty :
            주문수량

        nPrice :
            주문가격

        sHogaGb :
            거래구분

        sOrgOrderNo :
            원주문번호
        '''
        self.dynamicCall("SendOrder(QString, QString, QString, QString, QString, QString, QString, QString, QString)",
                         TrCode.SEND_ORDER.value, sScrNo, sAccNo, nOrderType.value, sCode, nQty, nPrice, sHogaGb, sOrgOrderNo)

    def parse_realtime(self, sCode: str, realtimeDataList: List[RealTimeDataEnum]) -> Dict[RealTimeDataEnum, Any]:
        '''
        realtime_callback이 호출 되었을 경우에만 사용이 가능하다.

        실시간 데이터 이벤트가 발생했을 때, FID 들을 파싱하여 가져오는 메소드
        '''
        realtime_data = {}

        for realtime_enum in realtimeDataList:
            realtime_data[realtime_enum] = self.dynamicCall("GetCommRealData(QString, QString)", sCode, realtime_enum.value)

        return realtime_data

    def _set_input_values(self, input_value: Dict[str, str]):
        '''
        SetInputVlaue() 동적 호출 iteration 용도
        '''
        for k, v in input_value.items():
            self.dynamicCall("SetInputValue(QString, QString)", k, v)

    def _tr_data_slot(self, sScrNo, sRQName, sTrCode, sPrevNext):
        '''
        CommRqData 처리용 슬롯
        '''
        _ = (sScrNo, sPrevNext)     # warning avoid

        n_record = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)  # tr데이터 중, 멀티데이터의 레코드 개수를 받아옴.

        self.__tr_data_temp = {}     # 이전에 저장되어 있던 임시 tr_data 삭제.
        self.__tr_data_temp["single_data"] = {}     # empty dict 선언
        for s_data in self.__tr_rq_single_data:
            self.__tr_data_temp["single_data"][s_data] = self.dynamicCall(
                "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, s_data).replace(" ", "")

        self.__tr_data_temp["multi_data"] = []
        for i in range(n_record):
            m_data_dict_temp = {}   # 멀티데이터에서 레코드 하나에 담길 딕셔너리 선언
            for m_data in self.__tr_rq_multi_data:
                m_data_dict_temp[m_data] = self.dynamicCall(
                    "GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, m_data)
            self.__tr_data_temp["multi_data"].append(m_data_dict_temp)
        self.__global_eventloop.exit()

    def _realtime_data_slot(self, sCode, sRealType, sRealData):
        '''
        realtime data 처리용 슬롯
        '''
        self.__realtime_data_callback(sCode, sRealType, sRealData)

    def _login_slot(self, errNo):
        print(ErrCode(errNo))
        self.__global_eventloop.exit()

    def _send_condition_slot(self, _sScrNo, sCodeList, _sCondName, _nIndex, _nNext):
        '''
        SendCondition 처리용 슬롯
        '''
        self.__condition_stock_list = sCodeList[:-1].split(";")
        self.__global_eventloop.exit()

    def _condition_ver_slot(self, _lRet, _sMsg):
        '''
        GetConditionLoad 처리용 슬롯
        '''
        self.__condition_name_list = []  # 이전에 저장되어 있던 조건식 들을 삭제한다.
        condition_name_list = self.dynamicCall("GetConditionNameList()")

        for cond_index_name in condition_name_list[:-1].split(";"):
            self.__condition_name_list.append(cond_index_name.split("^"))

        self.__global_eventloop.exit()

    def _server_msg_slot(self, _sScrNo, sRQName, sTrCode, sMsg):
        '''
        서버 통신 응답 처리용 슬롯
        '''
        if self.__server_msg_callback is not None:
            self.__server_msg_callback(TrCode(sRQName.replace(" ", ""), sMsg))

    def _chejan_data_slot(self, sGubun, nItemCnt, sFidList):
        '''체결 잔고데이터 이벤트 처리용 슬롯
        '''
        fid_list = sFidList[:-1].split(";")

        chejan_fid_data = {}
        for fid in fid_list:
            chejan_fid_data[fid] = self.dynamicCall("GetChejanData(QString)", fid)

        if self.__chejan_data_callback is not None:
            self.__chejan_data_callback(chejan_fid_data)

    def __reg_all_slot(self):
        '''
        키움 API의 이벤트 슬롯을 전부 다 등록
        '''
        self.OnEventConnect.connect(self._login_slot)                 # 로그인 슬롯
        self.OnReceiveTrData.connect(self._tr_data_slot)              # Tr 데이터 슬롯
        self.OnReceiveConditionVer.connect(self._condition_ver_slot)  # 조건식 데이터 슬롯
        self.OnReceiveTrCondition.connect(self._send_condition_slot)  # 조건식 종목 슬롯
        self.OnReceiveRealData.connect(self._realtime_data_slot)      # 실시간 데이터 슬롯
        self.OnReceiveMsg.connect(self._server_msg_slot)
        self.OnReceiveChejanData.connect(self._chejan_data_slot)
