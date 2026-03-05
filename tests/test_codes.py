import pytest


def test_find_all_cards(iamport):
    result = iamport.find_all_cards()
    assert result is not None
    assert isinstance(result, list)


def test_find_card(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.find_card('invalid_code')


def test_find_all_banks(iamport):
    result = iamport.find_all_banks()
    assert result is not None
    assert isinstance(result, list)


def test_find_bank(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.find_bank('invalid_code')
