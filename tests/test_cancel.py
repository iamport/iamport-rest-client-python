# -*- coding: utf-8 -*-
from iamport import Iamport
import pytest


def test_cancel():
    iamport = Iamport()
    with pytest.raises(TypeError):
        iamport.cancel(imp_uid='nothing')
    with pytest.raises(Iamport.ResponseError):
        iamport.cancel('reason', imp_uid='nothing')
    try:
        iamport.cancel('reason', imp_uid='nothing')
    except Iamport.ResponseError as e:
        assert e.code == 1
        assert e.message == u'취소할 결제건이 존재하지 않습니다.'
