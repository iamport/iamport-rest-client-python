# -*- coding: utf-8 -*-


def test_find(iamport):
    result = iamport.find(imp_uid='test')
    assert dict == type(result)
    result = iamport.find(merchant_uid='test')
    assert dict == type(result)
