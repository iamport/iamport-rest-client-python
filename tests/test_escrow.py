import pytest


def test_find_escrow_logis(iamport):
    with pytest.raises(iamport.HttpError):
        iamport.find_escrow_logis('imp_test_uid')


def test_create_escrow_logis_missing_params(iamport):
    with pytest.raises(KeyError) as e:
        iamport.create_escrow_logis('imp_test_uid')
    assert 'Essential parameter is missing!: sender' in str(e.value)


def test_create_escrow_logis(iamport):
    sender = {'name': 'sender', 'tel': '01012345678'}
    receiver = {'name': 'receiver', 'tel': '01087654321'}
    logis = {'company': 'CJ', 'invoice': '1234567890', 'sent_at': 0}

    with pytest.raises(iamport.HttpError):
        iamport.create_escrow_logis(
            'imp_test_uid',
            sender=sender,
            receiver=receiver,
            logis=logis,
        )


def test_update_escrow_logis_missing_params(iamport):
    with pytest.raises(KeyError) as e:
        iamport.update_escrow_logis('imp_test_uid')
    assert 'Essential parameter is missing!: sender' in str(e.value)


def test_update_escrow_logis(iamport):
    sender = {'name': 'sender', 'tel': '01012345678'}
    receiver = {'name': 'receiver', 'tel': '01087654321'}
    logis = {'company': 'CJ', 'invoice': '1234567890', 'sent_at': 0}

    with pytest.raises(iamport.HttpError):
        iamport.update_escrow_logis(
            'imp_test_uid',
            sender=sender,
            receiver=receiver,
            logis=logis,
        )
