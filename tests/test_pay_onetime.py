# -*- coding: utf-8 -*-


def test_pay_onetime(iamport):
    # Without 'card_number'
    payload_notEnough = {
        'merchant_uid': 'qwer1234',
        'amount': 5000,
        'expiry': '2019-03',
        'birth': '500203',
        'pwd_2digit': '19'
    }

    try:
        iamport.pay_onetime(**payload_notEnough)
    except KeyError as e:
        assert "Essential parameter is missing!: card_number" in str(e)

    payload_full = {
        'merchant_uid': 'qwer1234',
        'amount': 5000,
        'card_number': '4092-0230-1234-1234',
        'expiry': '2019-03',
        'birth': '500203',
        'pwd_2digit': '19'
    }

    try:
        iamport.pay_onetime(**payload_full)
    except iamport.ResponseError as e:
        assert e.code == -1
        assert u'카드정보 인증에 실패하였습니다.' in e.message
