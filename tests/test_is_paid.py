# -*- coding: utf-8 -*-


def test_is_paid_with_response(iamport, merchant_uid):
    mocked_response = {
        'status': 'paid',
        'amount': 1000,
    }
    assert True is iamport.is_paid(amount=1000, response=mocked_response, merchant_uid=merchant_uid)


def test_is_paid_without_response(iamport):
    assert False is iamport.is_paid(amount=1000, merchant_uid='qwer1234')  # 고정 필요
