import pytest


def test_partner_receipt(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.partner_receipt(
            'imp_test_uid',
            data={'key': 'value'},
        )
