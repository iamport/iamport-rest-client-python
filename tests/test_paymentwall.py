import pytest


def test_paymentwall_delivery_missing_params(iamport):
    with pytest.raises(KeyError) as e:
        iamport.paymentwall_delivery()
    assert 'Essential parameter is missing!: imp_uid' in str(e.value)


def test_paymentwall_delivery(iamport):
    with pytest.raises((iamport.HttpError, iamport.ResponseError)):
        iamport.paymentwall_delivery(
            imp_uid='imp_test_uid',
            merchant_uid='test_merchant_uid',
            type='physical',
            status='delivering',
            estimated_delivery_datetime='2025-12-31',
            estimated_update_datetime='2025-12-31',
            refundable=True,
            shipping_address_email='test@test.com',
        )
