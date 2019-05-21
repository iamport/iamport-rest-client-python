# -*- coding: utf-8 -*-
import pytest


def test_find(iamport, merchant_uid):
    with pytest.raises(KeyError):
        iamport.find()
    with pytest.raises(iamport.HttpError):
        iamport.find(imp_uid='test')
    with pytest.raises(iamport.HttpError):
        iamport.find(merchant_uid=merchant_uid)
