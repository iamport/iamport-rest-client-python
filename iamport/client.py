# -*- coding: utf-8 -*-
import requests

__all__ = ['IAMPORT_API_URL', 'Iamport']

IAMPORT_API_URL = 'https://api.iamport.kr/'


class Iamport(object):
    def __init__(self, imp_key, imp_secret, imp_url=IAMPORT_API_URL):
        self.imp_key = imp_key
        self.imp_secret = imp_secret
        self.imp_url = imp_url
        requests_session = requests.Session()
        requests_adapters = requests.adapters.HTTPAdapter(max_retries=3)
        requests_session.mount('https://', requests_adapters)
        self.requests_session = requests_session

    class ResponseError(Exception):
        def __init__(self, code=None, message=None):
            self.code = code
            self.message = message

    @staticmethod
    def get_response(response):
        if response.status_code != requests.codes.ok:
            return {}
        result = response.json()
        if result['code'] != 0:
            raise Iamport.ResponseError(result.get('code'), result.get('message'))
        return result.get('response')

    def _get_token(self):
        url = '{}users/getToken'.format(self.imp_url)
        payload = {'imp_key': self.imp_key,
                   'imp_secret': self.imp_secret}
        response = self.requests_session.post(url, data=payload)
        return self.get_response(response).get('access_token')

    def get_headers(self):
        return {'X-ImpTokenHeader': self._get_token()}

    def _get(self, url, payload=None):
        headers = self.get_headers()
        response = self.requests_session.get(url, headers=headers, params=payload)
        return self.get_response(response)

    def _post(self, url, payload=None):
        headers = self.get_headers()
        response = self.requests_session.post(url, headers=headers, data=payload)
        return self.get_response(response)

    def find_by_merchant_uid(self, merchant_uid):
        url = '{}payments/find/{}'.format(self.imp_url, merchant_uid)
        return self._get(url)

    def find_by_imp_uid(self, imp_uid):
        url = '{}payments/{}'.format(self.imp_url, imp_uid)
        return self._get(url)

    def find(self, **kwargs):
        merchant_uid = kwargs.get('merchant_uid')
        if merchant_uid:
            return self.find_by_merchant_uid(merchant_uid)
        try:
            imp_uid = kwargs['imp_uid']
        except KeyError:
            raise KeyError('merchant_uid or imp_uid is required')
        return self.find_by_imp_uid(imp_uid)

    def _cancel(self, payload):
        url = '{}payments/cancel'.format(self.imp_url)
        return self._post(url, payload)

    def pay_onetime(self, **kwargs):
        url = '{}subscribe/payments/onetime'.format(self.imp_url)
        for key in ['merchant_uid', 'amount', 'card_number', 'expiry', 'birth', 'pwd_2digit']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)

        return self._post(url, kwargs)

    def pay_again(self, **kwargs):
        url = '{}subscribe/payments/again'.format(self.imp_url)
        for key in ['customer_uid', 'merchant_uid', 'amount']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)

        return self._post(url, kwargs)

    def pay_foreign(self, **kwargs):
        url = '{}subscribe/payments/foreign'.format(self.imp_url)
        for key in ['merchant_uid', 'amount', 'card_number', 'expiry']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)

        return self._post(url, kwargs)

    def cancel_by_merchant_uid(self, merchant_uid, reason, **kwargs):
        payload = {'merchant_uid': merchant_uid, 'reason': reason}
        if kwargs:
            payload.update(kwargs)
        return self._cancel(payload)

    def cancel_by_imp_uid(self, imp_uid, reason, **kwargs):
        payload = {'imp_uid': imp_uid, 'reason': reason}
        if kwargs:
            payload.update(kwargs)
        return self._cancel(payload)

    def cancel(self, reason, **kwargs):
        imp_uid = kwargs.pop('imp_uid', None)
        if imp_uid:
            return self.cancel_by_imp_uid(imp_uid, reason, **kwargs)

        merchant_uid = kwargs.pop('merchant_uid', None)
        if merchant_uid is None:
            raise KeyError('merchant_uid or imp_uid is required')
        return self.cancel_by_merchant_uid(merchant_uid, reason, **kwargs)

    def is_paid(self, amount, **kwargs):
        response = kwargs.get('response')
        if not response:
            response = self.find(**kwargs)
        status = response.get('status')
        response_amount = response.get('amount')
        return status == 'paid' and response_amount == amount
