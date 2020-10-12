# -*- coding: utf-8 -*-
import time
from iamport.exceptions import ResponseError


def test_pay_schedule(iamport):
    schedule_at = int(time.time() + 1000)

    payload_without_customer_uid = {
        # without 'customer_uid'
        'schedules': [
            {
                'merchant_uid': 'pay_schedule_{}'.format(str(time.time())),
                'schedule_at': schedule_at,
                'amount': 2001,
                'name': '주문명1',
                'buyer_name': '주문자명',
                'buyer_email': '주문자 Email주소',
                'buyer_tel': '주문자 전화번호',
                'buyer_addr': '주문자 주소',
                'buyer_postcode': '주문자 우편번호'
            },
        ],
    }

    try:
        iamport.pay_schedule(**payload_without_customer_uid)
    except KeyError as e:
        assert 'customer_uid is required' in str(e)

    payload_without_merchant_uid = {
        'customer_uid': '00000000',
        'schedules': [
            {
                # without 'merchant_uid'
                'schedule_at': schedule_at,
                'amount': 10000,
                'name': '주문명2',
                'buyer_name': '주문자명',
                'buyer_email': '주문자 Email주소',
                'buyer_tel': '주문자 전화번호',
                'buyer_addr': '주문자 주소',
                'buyer_postcode': '주문자 우편번호'
            },
        ],
    }

    try:
        iamport.pay_schedule(**payload_without_merchant_uid)
    except KeyError as e:
        assert 'Essential parameter is missing!: merchant_uid' in str(e)

    payload_full = {
        'customer_uid': '00000000',
        'schedules': [
            {
                'merchant_uid': 'pay_schedule_{}'.format(str(time.time())),
                'schedule_at': schedule_at,
                'amount': 5000,
                'name': '주문명',
                'buyer_name': '주문자명',
                'buyer_email': '주문자 Email주소',
                'buyer_tel': '주문자 전화번호',
                'buyer_addr': '주문자 주소',
                'buyer_postcode': '주문자 우편번호'
            },
        ],
    }

    try:
        iamport.pay_schedule(**payload_full)
    except ResponseError as e:
        assert e.code == 1


def test_pay_schedule_protobuf(iamport):
    schedule_at = int(time.time() + 1000)

    payload_full = {
        'customer_uid': '00000000',
        'schedules': [
            {
                'merchant_uid': 'pay_schedule_{}'.format(str(time.time())),
                'schedule_at': schedule_at,
                'amount': 5000,
                'name': '주문명',
                'buyer_name': '주문자명',
                'buyer_email': '주문자 Email주소',
                'buyer_tel': '주문자 전화번호',
                'buyer_addr': '주문자 주소',
                'buyer_postcode': '주문자 우편번호'
            },
        ],
    }

    try:
        iamport.pay_schedule_protobuf(**payload_full)
    except ResponseError as e:
        assert e.code == 1


def test_get_scheduled_payment_list_by_merchant_uid(iamport):
    query = {
        'merchant_uid': 'your_merchant_uid0003'
    }

    resp = iamport.get_scheduled_payment_list_by_merchant_uid(**query)
    if resp.merchant_uid == '':
        print(resp)
        raise ResponseError


def test_get_scheduled_payment_list_by_customer_uid(iamport):
    query = {
        'customer_uid': 'wenli_customer01',
        'from': 1601474849,
        'to': 1602474849
    }

    resp = iamport.get_scheduled_payment_list_by_customer_uid(**query)
    if len(resp.list) != 0:
        print(resp.list)
        raise ResponseError

