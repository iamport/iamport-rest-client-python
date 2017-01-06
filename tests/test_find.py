# -*- coding: utf-8 -*-
import pytest


def test_find(iamport):
    with pytest.raises(KeyError):
        iamport.find()
    result = iamport.find(imp_uid='test')
    assert dict == type(result)
    result = iamport.find(merchant_uid='test')
    assert dict == type(result)
