# -*- coding: utf-8 -*-


def test_get_billding_key(iamport):
    # Without 'card_number'
    payload_notEnough = {
        'expiry': '2019-03',
        'birth': '500203',
        'pwd_2digit': '19'
    }

    test_customer_uid = 'test_customer_uid'

    try:
        iamport.get_billing_key(test_customer_uid, **payload_notEnough)
    except KeyError as e:
        assert "Essential parameter is missing!: card_number" in str(e)

    payload_full = {
        'card_number': '4092-0230-1234-1234',
        'expiry': '2019-03',
        'birth': '500203',
        'pwd_2digit': '19'
    }

    try:
        iamport.get_billing_key(test_customer_uid, **payload_full)
    except iamport.ResponseError as e:
        assert e.code == -1
        assert u'유효기간 오류' in e.message


def test_delete_billing_key(iamport):
    # Without 'card_number'

    test_customer_uid = 'test_customer_uid'

    try:
        iamport.delete_billing_key(test_customer_uid)
    except iamport.ResponseError as e:
        assert e.code == 1
        assert u'등록된 정보를 찾을 수 없습니다' in e.message
