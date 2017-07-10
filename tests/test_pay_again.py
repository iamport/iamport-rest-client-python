# -*- coding: utf-8 -*-


def test_pay_again(iamport):
    # Without 'customer_uid'
    payload_notEnough = {
        'merchant_uid': '1234qwer',
        'amount': 5000,
    }

    try:
        iamport.pay_again(**payload_notEnough)
    except KeyError as e:
        assert "Essential parameter is missing!: customer_uid" in str(e)

    payload_full = {
        'customer_uid': '00000000',
        'merchant_uid': '1234qwer',
        'amount': 5000,
    }

    try:
        iamport.pay_again(**payload_full)
    except iamport.ResponseError as e:
        assert e.code == 1
        assert u'등록되지 않은 구매자입니다.' in e.message
