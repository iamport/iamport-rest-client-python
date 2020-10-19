# -*- coding: utf-8 -*-
import pytest

from iamport.exceptions import HttpError


def test_find(iamport):
    with pytest.raises(KeyError):
        iamport.find()
    with pytest.raises(HttpError):
        iamport.find(imp_uid='test')
    with pytest.raises(HttpError):
        iamport.find(merchant_uid='âàáaā')

