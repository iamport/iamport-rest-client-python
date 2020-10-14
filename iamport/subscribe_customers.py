import json

from iamport.common import _Common
from iamport.protobuf_messages.subscribe_customers import subscribe_customers_pb2 as subscribe_customers
from iamport.protobuf_messages.subscribe import subscribe_pb2
from google.protobuf.json_format import MessageToJson


class Subscribe_customers(_Common):
    def get_multiple_billing_keys_by_customer(self, **kwargs):
        required_params = ['customer_uid']
        self._required_args_check(kwargs, required_params)

        msg = subscribe_customers.GetMultipleCustomerBillingKeyRequest(**kwargs)
        url = '{}subscribe/customers'.format(self.imp_url)
        payload = json.loads(MessageToJson(msg, preserving_proto_field_name=True))
        payload['customer_uid[]'] = payload['customer_uid']
        resp = self._get(url, payload=payload)
        return [subscribe_customers.CustomerBillingKey(**unit_resp) for unit_resp in resp]

    def delete_customer_billing_key(self, **kwargs):
        required_params = ['customer_uid']
        self._required_args_check(kwargs, required_params)

        msg = subscribe_customers.DeleteCustomerBillingKeyRequest(**kwargs)
        url = '{}subscribe/customers/{}'.format(self.imp_url, msg.customer_uid)
        resp = self._delete(url, payload=json.loads(MessageToJson(msg, preserving_proto_field_name=True)))
        return subscribe_customers.CustomerBillingKey(**resp)

    def get_customer_billing_key(self, **kwargs):
        required_params = ['customer_uid']
        self._required_args_check(kwargs, required_params)

        msg = subscribe_customers.GetCustomerBillingKeyRequest(**kwargs)
        url = '{}subscribe/customers/{}'.format(self.imp_url, msg.customer_uid)
        resp = self._get(url, payload=json.loads(MessageToJson(msg, preserving_proto_field_name=True)))
        return subscribe_customers.CustomerBillingKey(**resp)

    def insert_customer_billing_key(self, **kwargs):
        required_params = ['customer_uid', 'card_number', 'expiry', 'birth']
        self._required_args_check(kwargs, required_params)

        msg = subscribe_customers.InsertCustomerBillingKeyRequest(**kwargs)
        url = '{}subscribe/customers/{}'.format(self.imp_url, msg.customer_uid)
        resp = self._post(url, payload=json.loads(MessageToJson(msg, preserving_proto_field_name=True)))
        return subscribe_customers.CustomerBillingKey(**resp)

    def get_paid_by_billing_key_list(self, **kwargs):
        required_params = ['customer_uid']
        self._required_args_check(kwargs, required_params)

        msg = subscribe_customers.GetPaidByBillingKeyListRequest(**kwargs)
        url = '{}subscribe/customers/{}/payments'.format(self.imp_url, msg.customer_uid)
        resp = self._get(url, payload=json.loads(MessageToJson(msg, preserving_proto_field_name=True)))
        return subscribe_customers.NestedGetPaidByBillingKeyListData(**resp)

    def get_scheduled_payment_by_customer_list(self, **kwargs):
        required_params = ['customer_uid', 'from', 'to']
        self._required_args_check(kwargs, required_params)

        msg = subscribe_pb2.GetPaymentScheduleByCustomerRequest(**kwargs)
        url = '{}subscribe/customers/{}/schedules'.format(self.imp_url, msg.customer_uid)
        resp = self._get(url, payload=json.loads(MessageToJson(msg, preserving_proto_field_name=True)))
        return subscribe_customers.NestedGetPaidByBillingKeyListData(**resp)

