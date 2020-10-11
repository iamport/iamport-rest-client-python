from iamport.common import _Common
from iamport.protobuf_messages import payment_pb2
from google.protobuf.json_format import MessageToJson


class Payments(_Common):
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
    
    def prepare(self, merchant_uid, amount):
        url = '{}payments/prepare'.format(self.imp_url)
        payload = {'merchant_uid': merchant_uid, 'amount': amount}
        return self._post(url, payload)
    
    def prepare_validate(self, merchant_uid, amount):
        url = '{}payments/prepare/{}'.format(self.imp_url, merchant_uid)
        response = self._get(url)
        response_amount = response.get('amount')
        return response_amount == amount
    
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

