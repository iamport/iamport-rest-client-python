# -*- coding: utf-8 -*-
from iamport import Iamport
import pytest

def test_payOnetime(iamport):
    payload_notEnough = {
              'merchant_uid': '00000000'
            , 'amount': 5000
            #, 'card_number': '4092-0230-1234-1234'
            , 'expiry': '2019-03'
            , 'birth': '500203'
            , 'pwd_2digit': '19'
            }

    try:
        result = iamport.pay_onetime(**payload_notEnough)
    except KeyError as e:
        assert e.message == "Essential parameter is missing!: card_number"

    payload_full = {
              'merchant_uid': '00000000'
            , 'amount': 5000
            , 'card_number': '4092-0230-1234-1234'
            , 'expiry': '2019-03'
            , 'birth': '500203'
            , 'pwd_2digit': '19'
            }

    try:
        result = iamport.pay_onetime(**payload_full)
    except Iamport.ResponseError as e:
        assert e.code == -1
        assert u'카드정보 인증에 실패하였습니다.' in e.message
