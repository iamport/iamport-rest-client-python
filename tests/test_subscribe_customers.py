# -*- coding: utf-8 -*-
from iamport.exceptions import ResponseError, HttpError


def test_get_multiple_billing_keys_by_customer(iamport):
    customer_uids = ['00000000']
    payload = {
        'customer_uid': customer_uids
    }
    try:
        iamport.get_multiple_billing_keys_by_customer(**payload)
    except HttpError:
        pass
    except Exception:
        raise Exception('Unexpected exception')


def test_delete_customer_billing_key(iamport):
    payload = {
        'customer_uid': '00000000',
        'reason': 'test',
        'requester': 'test_script'
    }
    try:
        iamport.delete_customer_billing_key(**payload)
    except ResponseError as e:
        assert e.code == 1
    except Exception:
        raise Exception('Unexpected exception')


def test_insert_customer_billing_key(iamport):
    payload = {
        'customer_uid': '00000000',
        'pg': 'nice',
        'card_number': '5155-9449-1234-1234',
        'expiry': '1999-10',
        'birth': '560911',
        'pwd_2digit': '11',
    }
    try:
        iamport.insert_customer_billing_key(**payload)
    except ResponseError as e:
        assert e.code == -1
    except Exception:
        raise Exception('Unexpected exception')


def test_get_customer_billing_key(iamport):
    payload = {
        'customer_uid': '00000000',
    }
    try:
        iamport.get_customer_billing_key(**payload)
    except ResponseError as e:
        assert e.code == 1
    except Exception:
        raise Exception('Unexpected exception')


def test_get_paid_by_billing_key_list(iamport):
    payload = {
        'customer_uid': 'wenli_customer01',
    }
    resp = iamport.get_paid_by_billing_key_list(**payload)
    if len(resp.list) == 0:
        print(resp.list)
        raise Exception('Unexpected exception')


def test_get_scheduled_payment_by_customer_list(iamport):
    payload = {
        'customer_uid': 'wenli_customer01',
        'from': 1601474849,
        'to': 1602474849
    }
    resp = iamport.get_scheduled_payment_by_customer_list(**payload)
    if len(resp.list) != 0:
        print(resp.list)
        raise Exception('Unexpected exception')

