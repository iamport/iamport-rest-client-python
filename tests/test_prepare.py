# -*- coding: utf-8 -*-
import datetime
import time


def test_prepare(iamport):
    amount = 12000
    mid = 'merchant_%d' % time.mktime(datetime.datetime.now().timetuple())

    result = iamport.prepare(merchant_uid=mid, amount=amount)
    assert result['amount'] == amount
    assert result['merchant_uid'] == mid

    result = iamport.prepare_validate(merchant_uid=mid, amount=amount)
    assert result
