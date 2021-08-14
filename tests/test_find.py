import pytest


def test_find(iamport):
    with pytest.raises(KeyError):
        iamport.find()
    with pytest.raises(iamport.HttpError):
        iamport.find(imp_uid='test')
    with pytest.raises(iamport.HttpError):
        iamport.find(merchant_uid='âàáaā')
