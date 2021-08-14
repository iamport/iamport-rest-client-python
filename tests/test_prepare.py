import random
import string


def test_prepare(iamport):
    amount = 12000
    mid = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(10)
    )
    result = iamport.prepare(merchant_uid=mid, amount=amount)
    assert result['amount'] == amount
    assert result['merchant_uid'] == mid

    result = iamport.prepare_validate(merchant_uid=mid, amount=amount)
    assert result
