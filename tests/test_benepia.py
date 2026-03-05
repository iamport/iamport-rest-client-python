import pytest


def test_benepia_point_missing_params(iamport):
    with pytest.raises(KeyError) as e:
        iamport.benepia_point()
    assert 'Essential parameter is missing!: benepia_user' in str(e.value)


def test_benepia_point(iamport):
    with pytest.raises((iamport.HttpError, iamport.ResponseError)):
        iamport.benepia_point(
            benepia_user='test_user',
            benepia_password='test_password',
            channel_key='channel-key-test',
        )


def test_benepia_payment_missing_params(iamport):
    with pytest.raises(KeyError) as e:
        iamport.benepia_payment()
    assert 'Essential parameter is missing!: benepia_user' in str(e.value)


def test_benepia_payment(iamport):
    with pytest.raises((iamport.HttpError, iamport.ResponseError)):
        iamport.benepia_payment(
            benepia_user='test_user',
            benepia_password='test_password',
            merchant_uid='test_merchant_uid',
            amount=1000,
            name='test',
            channel_key='channel-key-test',
        )
