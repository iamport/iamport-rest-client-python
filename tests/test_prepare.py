# -*- coding: utf-8 -*-

def test_prepare(iamport, merchant_uid):
    amount = 12000

    result = iamport.prepare(merchant_uid=merchant_uid, amount=amount)
    assert result['amount'] == amount
    assert result['merchant_uid'] == merchant_uid

    result = iamport.prepare_validate(merchant_uid=merchant_uid, amount=amount)
    assert result
