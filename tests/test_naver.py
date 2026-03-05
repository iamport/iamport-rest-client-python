import pytest


def test_naver_cancel(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_cancel('imp_test_uid')


def test_naver_approve_cancel(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_approve_cancel('imp_test_uid')


def test_naver_ship(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_ship(
            'imp_test_uid',
            delivery_method='DELIVERY',
            dispatched_at=1478150985,
        )


def test_naver_ship_exchanged(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_ship_exchanged(
            'imp_test_uid',
            delivery_method='DELIVERY',
        )


def test_naver_collect_exchanged(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_collect_exchanged('imp_test_uid')


def test_naver_place(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_place('imp_test_uid')


def test_naver_request_return(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_request_return(
            'imp_test_uid',
            delivery_method='RETURN_DELIVERY',
        )


def test_naver_approve_return(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_approve_return('imp_test_uid')


def test_naver_reject_return(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_reject_return('imp_test_uid', memo='reject memo')


def test_naver_withhold_return(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_withhold_return('imp_test_uid', memo='withhold memo')


def test_naver_resolve_return(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_resolve_return('imp_test_uid')


def test_naver_deposit_point(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_deposit_point('imp_test_uid')


def test_naver_confirm(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_confirm('imp_test_uid')


def test_naver_product_orders(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_product_orders('imp_test_uid')


def test_naver_single_product_order(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_single_product_order('product_order_test')


def test_naver_reviews_missing_params(iamport):
    with pytest.raises(KeyError) as e:
        iamport.naver_reviews()
    assert 'Essential parameter is missing!: channel_key' in str(e.value)


def test_naver_reviews(iamport):
    with pytest.raises((iamport.HttpError, iamport.ResponseError)):
        iamport.naver_reviews(
            channel_key='channel-key-test',
            review_type='general',
            **{'from': 0, 'to': 9999999999}
        )


def test_naver_cash_amount(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.naver_cash_amount('imp_test_uid')
