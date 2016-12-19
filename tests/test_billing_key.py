# -*- coding: utf-8 -*-


def test_billing_key(iamport):
    customer_id = None
    try:
        iamport.get_billing_key(customer_id)
    except iamport.ResponseError as e:
        assert e.code != 0

    customer_id = 1000
    payload = {
        'amount': 0,
        'card_number': '0000-0000-0000-0000',
        'expiry': '2019-03',
        'birth': '500203',
        'pwd_2digit': '19',
        'customer_id': customer_id
    }
    try:
        iamport.set_billing_key(**payload)
    except iamport.ResponseError as e:
        assert e.code != 0

    try:
        iamport.get_billing_key(customer_id)
    except iamport.ResponseError as e:
        assert e.code == 0

    iamport.delete_billing_key(customer_id)

    try:
        iamport.get_billing_key(customer_id)
    except iamport.ResponseError as e:
        assert e.code != 0


def test_set_billing_key(iamport):
    payload_no_pwd2_digit = {
        'amount': 0,
        'card_number': '0000-0000-0000-0000',
        'expiry': '2019-03',
        'birth': '500203',
        'customer_id': 1000
    }
    try:
        iamport.set_billing_key(**payload_no_pwd2_digit)
    except KeyError as e:
        assert "Essential parameter is missing!: pwd2_digit" in str(e)

    payload_no_card_number = {
        'amount': 0,
        'card_number': '0000-0000-0000-0000',
        'expiry': '2019-03',
        'birth': '500203',
        'customer_id': 1000
    }
    try:
        iamport.set_billing_key(**payload_no_card_number)
    except KeyError as e:
        assert "Essential parameter is missing!: card_number" in str(e)

    payload_full = {
        'amount': 0,
        'card_number': '4092-0230-1234-1234',
        'expiry': '2019-03',
        'birth': '500203',
        'pwd_2digit': '19',
        'customer_id': 1000
    }
    try:
        iamport.set_billing_key(**payload_full)
    except iamport.ResponseError as e:
        assert e.code == -1
        assert u'카드정보 인증 및 빌키 발급에 실패하였습니다.' in e.message