# -*- coding: utf-8 -*-


def test_customer_get(iamport):
    customer_uid = '000000'
    try:
        iamport.customer_get(customer_uid)
    except iamport.ResponseError as e:
        # not exsting customer
        pass
