import pytest


def test_find_certification(iamport):
    imp_uid = 'imp_12341234'

    with pytest.raises(iamport.HttpError) as e:
        iamport.find_certification(imp_uid)
        assert u'인증결과가 존재하지 않습니다.' == e.message

    with pytest.raises(iamport.HttpError) as e:
        iamport.cancel_certification(imp_uid)
        assert u'인증결과가 존재하지 않습니다.' == e.message
