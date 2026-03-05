import pytest


def test_payco_update_order_status(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.payco_update_order_status(
            'imp_test_uid',
            status='DELIVERY_START',
        )
