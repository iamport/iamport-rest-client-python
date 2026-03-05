import pytest


def test_kcpquick_delete_member_missing_params(iamport):
    with pytest.raises(KeyError) as e:
        iamport.kcpquick_delete_member('test_member')
    assert 'Essential parameter is missing!: site_code' in str(e.value)


def test_kcpquick_delete_member(iamport):
    with pytest.raises((iamport.HttpError, iamport.ResponseError)):
        iamport.kcpquick_delete_member(
            'test_member',
            site_code='T0000',
            partner_type='STORE',
            partner_subtype='GENERAL',
        )


def test_kcpquick_payment_money_missing_params(iamport):
    with pytest.raises(KeyError) as e:
        iamport.kcpquick_payment_money()
    assert 'Essential parameter is missing!: member_id' in str(e.value)


def test_kcpquick_payment_money(iamport):
    with pytest.raises((iamport.HttpError, iamport.ResponseError)):
        iamport.kcpquick_payment_money(
            member_id='test_member',
            channel_key='channel-key-test',
            merchant_uid='test_merchant_uid',
            name='test',
            amount=1000,
        )
