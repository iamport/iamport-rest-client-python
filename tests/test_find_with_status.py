def test_find_with_status(iamport):
    # Without 'customer_uid'
    cancelled_payload = {
        'merchant_uid': '1234qwer',
        'status': 'cancelled'
    }

    paid_payload = {
        'merchant_uid': '1234qwer',
        'status': 'paid'
    }

    empty_payload = {
        'merchant_uid': '1234qwer',
    }

    try:
        res = iamport.find_by_merchant_uid(**cancelled_payload)
    except iamport.HttpError as e:
        assert e.code == 404

    res = iamport.find_by_merchant_uid(**empty_payload)
    assert res['merchant_uid'] == '1234qwer'

    res = iamport.find_by_merchant_uid(**paid_payload)
    assert res['merchant_uid'] == '1234qwer'
