

def test_pay_foreign(iamport):
    payload = {
        'merchant_uid': 'uid',
        'amount': 100,
        'card_number': 'card-number',
    }
    try:
        iamport.pay_foreign(**payload)
    except KeyError as e:
        assert "Essential parameter is missing!: expiry" in str(e)

    payload.update({
        'expiry': '2016-08',
    })

    try:
        iamport.pay_foreign(**payload)
    except iamport.ResponseError as e:
        assert e.code == -1
