# -*- coding: utf-8 -*-


def test_customer_create(iamport):
    # Without 'card_number'
    payload_notEnough = {
        'customer_uid': 'customer_1234',
        'expiry': '2019-03',
        'birth': '500203',
    }

    try:
        iamport.customer_create(**payload_notEnough)
    except KeyError as e:
        assert "Essential parameter is missing!: card_number" in str(e)

    payload_full = {
        'customer_uid': 'customer_1234',
        'expiry': '2019-03',
        'birth': '500203',
        'card_number': '4092-0230-1234-1234',
    }

    try:
        iamport.customer_create(**payload_full)
    except iamport.ResponseError as e:
        assert e.code == -1
        assert u'카드정보 인증 및 빌키 발급에 실패하였습니다.' in e.message
