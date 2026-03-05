import pytest


def test_create_vbank_missing_params(iamport):
    with pytest.raises(KeyError) as e:
        iamport.create_vbank()
    assert 'Essential parameter is missing!: channel_key' in str(e.value)


def test_create_vbank(iamport):
    with pytest.raises((iamport.HttpError, iamport.ResponseError)):
        iamport.create_vbank(
            channel_key='channel-key-test',
            merchant_uid='test_merchant_uid',
            amount=1000,
            vbank_code='004',
            vbank_due=9999999999,
        )


def test_modify_vbank(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.modify_vbank('imp_test_uid', amount=2000)


def test_revoke_vbank(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.revoke_vbank_by_imp_uid('imp_test_uid')


def test_find_vbank_holder(iamport):
    with pytest.raises((iamport.HttpError, iamport.ResponseError)):
        iamport.find_vbank_holder('004', '12345678901234')
