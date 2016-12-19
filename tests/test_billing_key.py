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
        print(e)

    try:
        iamport.get_billing_key(customer_id)
    except iamport.ResponseError as e:
        assert e.code == 0

    iamport.delete_billing_key(customer_id)

    try:
        iamport.get_billing_key(customer_id)
    except iamport.ResponseError as e:
        assert e.code != 0
