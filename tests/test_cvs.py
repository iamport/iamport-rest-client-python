import pytest


def test_create_cvs_missing_params(iamport):
    with pytest.raises(KeyError) as e:
        iamport.create_cvs()
    assert 'Essential parameter is missing!: channel_key' in str(e.value)


def test_create_cvs(iamport):
    with pytest.raises((iamport.HttpError, iamport.ResponseError)):
        iamport.create_cvs(
            channel_key='channel-key-test',
            merchant_uid='test_merchant_uid',
            amount=1000,
        )


def test_revoke_cvs(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.revoke_cvs('imp_test_uid')
