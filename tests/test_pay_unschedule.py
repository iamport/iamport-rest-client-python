# -*- coding: utf-8 -*-


def test_pay_unschedule(iamport):
    payload_without_customer_uid = {
        # without 'customer_uid'
        'merchant_uid': '00000000',
    }

    try:
        iamport.pay_unschedule(**payload_without_customer_uid)
    except KeyError as e:
        assert 'customer_uid is required' in str(e)

    payload_full = {
        'customer_uid': '00000000',
        'merchant_uid': '87654321',
    }

    try:
        iamport.pay_unschedule(**payload_full)
    except iamport.ResponseError as e:
        assert e.code == 1
        assert u'취소할 예약결제 기록이 존재하지 않습니다.' in e.message
