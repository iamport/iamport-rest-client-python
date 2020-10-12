# -*- coding: utf-8 -*-
from iamport.exceptions import ResponseError


def test_pay_again(iamport):
    # Without 'customer_uid'
    payload_notEnough = {
        'merchant_uid': '1234qwer',
        'amount': 5000,
    }

    try:
        iamport.pay_again(**payload_notEnough)
    except KeyError as e:
        assert "Essential parameter is missing!: customer_uid" in str(e)

    payload_full = {
        'customer_uid': '00000000',
        'merchant_uid': '1234qwer',
        'amount': 5000,
    }

    try:
        iamport.pay_again(**payload_full)
    except ResponseError as e:
        assert e.code == -1


def test_pay_again_protobuf(iamport):
    payload_full = {
        'name': 'test_product',
        'customer_uid': '00000000',
        'merchant_uid': '1234qwer',
        'amount': 5000
    }

    try:
        iamport.pay_again_protobuf(**payload_full)
    except ResponseError as e:
        assert e.code == -1

