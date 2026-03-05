import pytest


def test_find_tier(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.find_tier('test_tier_code')
