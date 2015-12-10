# -*- coding: utf-8 -*-
from iamport import Iamport


def test_find():
    iamport = Iamport()
    result = iamport.find(imp_uid='test')
    assert dict == type(result)
    result = iamport.find(merchant_uid='test')
    assert dict == type(result)
