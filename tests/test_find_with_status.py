def test_find_with_status(iamport):
    try:
        iamport.find_by_merchant_uid(merchant_uid='1234qwer',
                                     status='cancelled')
    except iamport.HttpError as e:
        assert e.code == 404

    res = iamport.find_by_merchant_uid(merchant_uid='1234qwer')
    assert res['merchant_uid'] == '1234qwer'

    res = iamport.find_by_merchant_uid(merchant_uid='1234qwer', status='paid')
    assert res['merchant_uid'] == '1234qwer'
