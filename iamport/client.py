# -*- coding: utf-8 -*-
import requests

TEST_IMP_KEY = 'imp_apikey'
TEST_IMP_SECRET = 'ekKoeW8RyKuT0zgaZsUtXXTLQ4AhPFW3ZGseDA6bkA5lamv9OqDMnxyeB9wqOsuO9W3Mx9YSJ4dTqJ3f'
IAMPORT_API_URL = 'https://api.iamport.kr/'


class Iamport(object):
    def __init__(self,
                 imp_key=TEST_IMP_KEY,
                 imp_secret=TEST_IMP_SECRET,
                 imp_url=IAMPORT_API_URL):
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
        if result['code'] is not 0:
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

    def cancel_by_merchant_uid(self, merchant_uid, reason):
        payload = {'merchant_uid': merchant_uid, 'reason': reason}
        return self._cancel(payload)

    def cancel_by_imp_uid(self, imp_uid, reason):
        payload = {'imp_uid': imp_uid, 'reason': reason}
        return self._cancel(payload)

    def cancel(self, reason, **kwargs):
        merchant_uid = kwargs.get('merchant_uid')
        if merchant_uid:
            return self.cancel_by_merchant_uid(merchant_uid, reason)
        try:
            imp_uid = kwargs['imp_uid']
        except KeyError:
            raise KeyError('merchant_uid or imp_uid is required')
        return self.cancel_by_imp_uid(imp_uid, reason)

    def is_paid(self, amount, **kwargs):
        response = kwargs.get('response')
        if not response:
            response = self.find(**kwargs)
        status = response.get('status')
        response_amount = response.get('amount')
        return status == 'paid' and response_amount == amount
