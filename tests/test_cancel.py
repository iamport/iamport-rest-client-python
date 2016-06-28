# -*- coding: utf-8 -*-
from iamport import Iamport
import pytest


def test_cancel(iamport):
    with pytest.raises(TypeError):
        iamport.cancel(imp_uid='nothing')
    with pytest.raises(Iamport.ResponseError):
        iamport.cancel('reason', imp_uid='nothing')
    try:
        iamport.cancel('reason', imp_uid='nothing')
    except Iamport.ResponseError as e:
        assert e.code == 1
        assert e.message == u'취소할 결제건이 존재하지 않습니다.'


def test_partial_cancel(iamport):

    try:
        iamport.cancel('reason', imp_uid='nothing', amount=100)
    except Iamport.ResponseError as e:
        assert e.code == 1
        assert e.message == u'취소할 결제건이 존재하지 않습니다.'


def test_cancel_by_merchant_uid(iamport):

    payload = {
        'merchant_uid': 'any-merchant_uid',
        'reason': 'any-reason',
    }

    try:
        iamport.cancel(**payload)
    except Iamport.ResponseError as e:
        assert e.code == 1
        assert e.message == u'취소할 결제건이 존재하지 않습니다.'


def test_cancel_by_imp_uid(iamport):

    payload = {
        'imp_uid': 'any-imp_uid',
        'reason': 'any-reason',
    }

    try:
        iamport.cancel(**payload)
    except Iamport.ResponseError as e:
        assert e.code == 1
        assert e.message == u'취소할 결제건이 존재하지 않습니다.'
