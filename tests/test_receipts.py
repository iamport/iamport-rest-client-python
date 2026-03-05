import pytest


def test_find_receipt(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.find_receipt('imp_test_uid')


def test_create_receipt(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.create_receipt('imp_test_uid', '0000000000')


def test_revoke_receipt(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.revoke_receipt('imp_test_uid')


def test_find_external_receipt(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.find_external_receipt('merchant_test_uid')


def test_create_external_receipt_missing_params(iamport):
    with pytest.raises(KeyError) as e:
        iamport.create_external_receipt('merchant_test_uid')
    assert 'Essential parameter is missing!: channel_key' in str(e.value)


def test_create_external_receipt(iamport):
    with pytest.raises((iamport.HttpError, iamport.ResponseError)):
        iamport.create_external_receipt(
            'merchant_test_uid',
            channel_key='channel-key-test',
            name='test',
            amount=1000,
            identifier='0000000000',
        )


def test_revoke_external_receipt(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.revoke_external_receipt('merchant_test_uid')
