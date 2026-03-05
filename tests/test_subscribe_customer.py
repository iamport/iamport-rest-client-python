import pytest


def test_customers_get(iamport):
    with pytest.raises((iamport.HttpError, iamport.ResponseError)):
        iamport.customers_get(['customer_uid_1', 'customer_uid_2'])


def test_customer_payments(iamport):
    with pytest.raises(iamport.ResponseError) as e:
        iamport.customer_payments('customer_uid_test')
    assert e.value.code != 0


def test_customer_schedules_missing_params(iamport):
    with pytest.raises(KeyError) as e:
        iamport.customer_schedules('customer_uid_test')
    assert 'Essential parameter is missing!: from' in str(e.value)


def test_customer_schedules(iamport):
    with pytest.raises(iamport.ResponseError) as e:
        iamport.customer_schedules(
            'customer_uid_test',
            **{'from': 0, 'to': 9999999999}
        )
    assert e.value.code != 0
