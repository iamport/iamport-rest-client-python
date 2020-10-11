import json

from iamport.common import _Common
from iamport.protobuf_messages import subscribe_pb2
from google.protobuf.json_format import MessageToJson


class Subscribe(_Common):
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
    
    def customer_create(self, **kwargs):
        customer_uid = kwargs.get('customer_uid')
        for key in ['customer_uid', 'card_number', 'expiry', 'birth']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        url = '{}subscribe/customers/{}'.format(self.imp_url, customer_uid)
        return self._post(url, kwargs)
    
    def customer_get(self, customer_uid):
        url = '{}subscribe/customers/{}'.format(self.imp_url, customer_uid)
        return self._get(url)
    
    def pay_foreign(self, **kwargs):
        url = '{}subscribe/payments/foreign'.format(self.imp_url)
        for key in ['merchant_uid', 'amount', 'card_number', 'expiry']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
    
        return self._post(url, kwargs)
    
    def pay_schedule(self, **kwargs):
        headers = self._get_headers()
        headers['Content-Type'] = 'application/json'
        url = '{}subscribe/payments/schedule'.format(self.imp_url)
        if 'customer_uid' not in kwargs:
            raise KeyError('customer_uid is required')
        for key in ['merchant_uid', 'schedule_at', 'amount']:
            for schedules in kwargs['schedules']:
                if key not in schedules:
                    raise KeyError('Essential parameter is missing!: %s' % key)
    
        return self._post(url, kwargs)
    
    def pay_unschedule(self, **kwargs):
        url = '{}subscribe/payments/unschedule'.format(self.imp_url)
        if 'customer_uid' not in kwargs:
            raise KeyError('customer_uid is required')
    
        return self._post(url, kwargs)
    
    ######################
    # Protobuf based API
    ######################
    
    def pay_onetime_protobuf(self, **kwargs):
        required_params = ['merchant_uid', 'amount', 'card_number', 'expiry', 'birth']
        self._required_args_check(kwargs, required_params)
    
        url = '{}subscribe/payments/onetime'.format(self.imp_url)
        msg = subscribe_pb2.OnetimePaymentRequest(**kwargs)
        resp = self._post(url, json.loads(MessageToJson(msg, preserving_proto_field_name=True)))
        return subscribe_pb2.OnetimePaymentResponse(**resp)

