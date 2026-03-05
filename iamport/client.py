import json

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

    class HttpError(Exception):
        def __init__(self, code=None, reason=None):
            self.code = code
            self.reason = reason

    @staticmethod
    def get_response(response):
        if response.status_code != requests.codes.ok:
            raise Iamport.HttpError(response.status_code, response.reason)
        result = response.json()
        if result['code'] != 0:
            raise Iamport.ResponseError(
                result.get('code'), result.get('message')
            )
        return result.get('response')

    def _get_token(self):
        url = '{}users/getToken'.format(self.imp_url)
        payload = {
            'imp_key': self.imp_key,
            'imp_secret': self.imp_secret
        }
        response = self.requests_session.post(
            url, headers={'Content-Type': 'application/json'},
            data=json.dumps(payload)
        )
        return self.get_response(response).get('access_token')

    def get_headers(self):
        return {'Authorization': self._get_token()}

    def _get(self, url, payload=None):
        headers = self.get_headers()
        response = self.requests_session.get(
            url, headers=headers, params=payload
        )
        return self.get_response(response)

    def _post(self, url, payload=None):
        headers = self.get_headers()
        headers['Content-Type'] = 'application/json'
        response = self.requests_session.post(
            url, headers=headers, data=json.dumps(payload)
        )
        return self.get_response(response)

    def _put(self, url, payload=None):
        headers = self.get_headers()
        headers['Content-Type'] = 'application/json'
        response = self.requests_session.put(
            url, headers=headers,
            data=json.dumps(payload) if payload else None
        )
        return self.get_response(response)

    def _delete(self, url, payload=None):
        headers = self.get_headers()
        if payload:
            headers['Content-Type'] = 'application/json'
            response = self.requests_session.delete(
                url, headers=headers, data=json.dumps(payload)
            )
        else:
            response = self.requests_session.delete(url, headers=headers)
        return self.get_response(response)

    # ===== Payments =====

    def find_by_status(self, status, **kwargs):
        url = '{}payments/status/{}'.format(self.imp_url, status)
        return self._get(url, kwargs)

    def find_by_merchant_uid(self, merchant_uid, status=None, **kwargs):
        url = '{}payments/find/{}'.format(self.imp_url, merchant_uid)
        if status is not None:
            url = '{}/{}'.format(url, status)
        return self._get(url, kwargs)

    def find_all_by_merchant_uid(self, merchant_uid, status=None, **kwargs):
        url = '{}payments/findAll/{}'.format(self.imp_url, merchant_uid)
        if status is not None:
            url = '{}/{}'.format(url, status)
        return self._get(url, kwargs)

    def find_by_imp_uid(self, imp_uid):
        url = '{}payments/{}'.format(self.imp_url, imp_uid)
        return self._get(url)

    def find_by_imp_uids(self, imp_uids):
        url = '{}payments'.format(self.imp_url)
        payload = {'imp_uid[]': imp_uids}
        return self._get(url, payload)

    def find_by_merchant_uids(self, merchant_uids):
        url = '{}payments'.format(self.imp_url)
        payload = {'merchant_uid[]': merchant_uids}
        return self._get(url, payload)

    def find(self, **kwargs):
        merchant_uid = kwargs.get('merchant_uid')
        if merchant_uid:
            return self.find_by_merchant_uid(merchant_uid)
        try:
            imp_uid = kwargs['imp_uid']
        except KeyError:
            raise KeyError('merchant_uid or imp_uid is required')
        return self.find_by_imp_uid(imp_uid)

    def find_balance(self, imp_uid):
        url = '{}payments/{}/balance'.format(self.imp_url, imp_uid)
        return self._get(url)

    def _cancel(self, payload):
        url = '{}payments/cancel'.format(self.imp_url)
        return self._post(url, payload)

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

    # ===== Payments Prepare =====

    def prepare(self, merchant_uid, amount):
        url = '{}payments/prepare'.format(self.imp_url)
        payload = {'merchant_uid': merchant_uid, 'amount': amount}
        return self._post(url, payload)

    def prepare_update(self, merchant_uid, amount, **kwargs):
        url = '{}payments/prepare'.format(self.imp_url)
        payload = {'merchant_uid': merchant_uid, 'amount': amount}
        if kwargs:
            payload.update(kwargs)
        return self._put(url, payload)

    def prepare_validate(self, merchant_uid, amount):
        url = '{}payments/prepare/{}'.format(self.imp_url, merchant_uid)
        response = self._get(url)
        response_amount = response.get('amount')
        return response_amount == amount

    # ===== Subscribe Payments =====

    def pay_onetime(self, **kwargs):
        url = '{}subscribe/payments/onetime'.format(self.imp_url)
        for key in [
            'merchant_uid', 'amount', 'card_number', 'expiry'
        ]:
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

    def pay_schedule(self, **kwargs):
        headers = self.get_headers()
        headers['Content-Type'] = 'application/json'
        url = '{}subscribe/payments/schedule'.format(self.imp_url)
        if 'customer_uid' not in kwargs:
            raise KeyError('customer_uid is required')
        for key in ['merchant_uid', 'schedule_at', 'amount']:
            for schedules in kwargs['schedules']:
                if key not in schedules:
                    raise KeyError('Essential parameter is missing!: %s' % key)

        return self._post(url, kwargs)

    def pay_schedule_get(self, merchant_id):
        url = '{}subscribe/payments/schedule/{}'.format(
            self.imp_url, merchant_id
        )
        return self._get(url)

    def pay_schedule_update(self, merchant_uid, schedule_at):
        url = '{}subscribe/payments/schedule/{}'.format(
            self.imp_url, merchant_uid
        )
        payload = {'merchant_uid': merchant_uid, 'schedule_at': schedule_at}
        return self._put(url, payload)

    def pay_schedule_reschedule(self, merchant_uid, schedule_at):
        url = '{}subscribe/payments/schedule/{}/reschedule'.format(
            self.imp_url, merchant_uid
        )
        payload = {'merchant_uid': merchant_uid, 'schedule_at': schedule_at}
        return self._post(url, payload)

    def pay_schedule_retry(self, merchant_uid):
        url = '{}subscribe/payments/schedule/{}/retry'.format(
            self.imp_url, merchant_uid
        )
        payload = {'merchant_uid': merchant_uid}
        return self._post(url, payload)

    def pay_schedule_get_between(self, **kwargs):
        url = '{}subscribe/payments/schedule'.format(self.imp_url)
        for key in ['schedule_from', 'schedule_to']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)

        return self._get(url, kwargs)

    def pay_schedule_get_by_customer(self, customer_uid, **kwargs):
        url = '{}subscribe/payments/schedule/customers/{}'.format(
            self.imp_url, customer_uid
        )
        for key in ['from', 'to']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        return self._get(url, kwargs)

    def pay_unschedule(self, **kwargs):
        url = '{}subscribe/payments/unschedule'.format(self.imp_url)
        if 'customer_uid' not in kwargs:
            raise KeyError('customer_uid is required')

        return self._post(url, kwargs)

    # ===== Subscribe Customers =====

    def customer_create(self, **kwargs):
        customer_uid = kwargs.get('customer_uid')
        for key in ['customer_uid', 'card_number', 'expiry']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        url = '{}subscribe/customers/{}'.format(self.imp_url, customer_uid)
        return self._post(url, kwargs)

    def customer_get(self, customer_uid):
        url = '{}subscribe/customers/{}'.format(self.imp_url, customer_uid)
        return self._get(url)

    def customers_get(self, customer_uids):
        url = '{}subscribe/customers'.format(self.imp_url)
        payload = {'customer_uid[]': customer_uids}
        return self._get(url, payload)

    def customer_delete(self, customer_uid):
        url = '{}subscribe/customers/{}'.format(self.imp_url, customer_uid)
        return self._delete(url)

    def customer_payments(self, customer_uid, **kwargs):
        url = '{}subscribe/customers/{}/payments'.format(
            self.imp_url, customer_uid
        )
        return self._get(url, kwargs)

    def customer_schedules(self, customer_uid, **kwargs):
        url = '{}subscribe/customers/{}/schedules'.format(
            self.imp_url, customer_uid
        )
        for key in ['from', 'to']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        return self._get(url, kwargs)

    # ===== Certifications =====

    def find_certification(self, imp_uid):
        url = '{}certifications/{}'.format(self.imp_url, imp_uid)
        return self._get(url)

    def cancel_certification(self, imp_uid):
        url = '{}certifications/{}'.format(self.imp_url, imp_uid)
        return self._delete(url)

    def request_certification_otp(self, **kwargs):
        url = '{}certifications/otp/request'.format(self.imp_url)
        for key in [
            'name', 'phone', 'birth', 'gender_digit',
            'carrier', 'channel_key'
        ]:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        return self._post(url, kwargs)

    def confirm_certification_otp(self, imp_uid, **kwargs):
        url = '{}certifications/otp/confirm/{}'.format(self.imp_url, imp_uid)
        return self._post(url, kwargs)

    # ===== VBanks =====

    def create_vbank(self, **kwargs):
        url = '{}vbanks'.format(self.imp_url)
        for key in [
            'channel_key', 'merchant_uid', 'amount',
            'vbank_code', 'vbank_due'
        ]:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        return self._post(url, kwargs)

    def modify_vbank(self, imp_uid, **kwargs):
        url = '{}vbanks/{}'.format(self.imp_url, imp_uid)
        payload = {'imp_uid': imp_uid}
        if kwargs:
            payload.update(kwargs)
        return self._put(url, payload)

    def revoke_vbank_by_imp_uid(self, imp_uid):
        url = '{}vbanks/{}'.format(self.imp_url, imp_uid)
        return self._delete(url)

    def find_vbank_holder(self, bank_code, bank_num):
        url = '{}vbanks/holder'.format(self.imp_url)
        payload = {'bank_code': bank_code, 'bank_num': bank_num}
        return self._get(url, payload)

    # ===== Escrows =====

    def find_escrow_logis(self, imp_uid):
        url = '{}escrows/logis/{}'.format(self.imp_url, imp_uid)
        return self._get(url)

    def create_escrow_logis(self, imp_uid, **kwargs):
        url = '{}escrows/logis/{}'.format(self.imp_url, imp_uid)
        for key in ['sender', 'receiver', 'logis']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        payload = {'imp_uid': imp_uid}
        payload.update(kwargs)
        return self._post(url, payload)

    def update_escrow_logis(self, imp_uid, **kwargs):
        url = '{}escrows/logis/{}'.format(self.imp_url, imp_uid)
        for key in ['sender', 'receiver', 'logis']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        payload = {'imp_uid': imp_uid}
        payload.update(kwargs)
        return self._put(url, payload)

    # ===== Receipts =====

    def find_receipt(self, imp_uid):
        url = '{}receipts/{}'.format(self.imp_url, imp_uid)
        return self._get(url)

    def create_receipt(self, imp_uid, identifier, **kwargs):
        url = '{}receipts/{}'.format(self.imp_url, imp_uid)
        payload = {'imp_uid': imp_uid, 'identifier': identifier}
        if kwargs:
            payload.update(kwargs)
        return self._post(url, payload)

    def revoke_receipt(self, imp_uid):
        url = '{}receipts/{}'.format(self.imp_url, imp_uid)
        return self._delete(url)

    def find_external_receipt(self, merchant_uid):
        url = '{}receipts/external/{}'.format(self.imp_url, merchant_uid)
        return self._get(url)

    def create_external_receipt(self, merchant_uid, **kwargs):
        url = '{}receipts/external/{}'.format(self.imp_url, merchant_uid)
        for key in ['channel_key', 'name', 'amount', 'identifier']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        payload = {'merchant_uid': merchant_uid}
        payload.update(kwargs)
        return self._post(url, payload)

    def revoke_external_receipt(self, merchant_uid):
        url = '{}receipts/external/{}'.format(self.imp_url, merchant_uid)
        return self._delete(url)

    # ===== Codes (Cards / Banks) =====

    def find_all_cards(self):
        url = '{}cards'.format(self.imp_url)
        return self._get(url)

    def find_card(self, card_standard_code):
        url = '{}cards/{}'.format(self.imp_url, card_standard_code)
        return self._get(url)

    def find_all_banks(self):
        url = '{}banks'.format(self.imp_url)
        return self._get(url)

    def find_bank(self, bank_standard_code):
        url = '{}banks/{}'.format(self.imp_url, bank_standard_code)
        return self._get(url)

    # ===== Naver =====

    def naver_cancel(self, imp_uid, **kwargs):
        url = '{}payments/{}/naver/cancel'.format(self.imp_url, imp_uid)
        payload = {'imp_uid': imp_uid}
        if kwargs:
            payload.update(kwargs)
        return self._post(url, payload)

    def naver_approve_cancel(self, imp_uid, **kwargs):
        url = '{}payments/{}/naver/approve-cancel'.format(
            self.imp_url, imp_uid
        )
        payload = {'imp_uid': imp_uid}
        if kwargs:
            payload.update(kwargs)
        return self._post(url, payload)

    def naver_ship(self, imp_uid, delivery_method, dispatched_at, **kwargs):
        url = '{}payments/{}/naver/ship'.format(self.imp_url, imp_uid)
        payload = {
            'imp_uid': imp_uid,
            'delivery_method': delivery_method,
            'dispatched_at': dispatched_at,
        }
        if kwargs:
            payload.update(kwargs)
        return self._post(url, payload)

    def naver_ship_exchanged(self, imp_uid, delivery_method, **kwargs):
        url = '{}payments/{}/naver/ship-exchanged'.format(
            self.imp_url, imp_uid
        )
        payload = {
            'imp_uid': imp_uid,
            'delivery_method': delivery_method,
        }
        if kwargs:
            payload.update(kwargs)
        return self._post(url, payload)

    def naver_collect_exchanged(self, imp_uid, **kwargs):
        url = '{}payments/{}/naver/collect-exchanged'.format(
            self.imp_url, imp_uid
        )
        payload = {'imp_uid': imp_uid}
        if kwargs:
            payload.update(kwargs)
        return self._post(url, payload)

    def naver_place(self, imp_uid, **kwargs):
        url = '{}payments/{}/naver/place'.format(self.imp_url, imp_uid)
        payload = {'imp_uid': imp_uid}
        if kwargs:
            payload.update(kwargs)
        return self._post(url, payload)

    def naver_request_return(self, imp_uid, delivery_method, **kwargs):
        url = '{}payments/{}/naver/request-return'.format(
            self.imp_url, imp_uid
        )
        payload = {
            'imp_uid': imp_uid,
            'delivery_method': delivery_method,
        }
        if kwargs:
            payload.update(kwargs)
        return self._post(url, payload)

    def naver_approve_return(self, imp_uid, **kwargs):
        url = '{}payments/{}/naver/approve-return'.format(
            self.imp_url, imp_uid
        )
        payload = {'imp_uid': imp_uid}
        if kwargs:
            payload.update(kwargs)
        return self._post(url, payload)

    def naver_reject_return(self, imp_uid, memo, **kwargs):
        url = '{}payments/{}/naver/reject-return'.format(
            self.imp_url, imp_uid
        )
        payload = {'imp_uid': imp_uid, 'memo': memo}
        if kwargs:
            payload.update(kwargs)
        return self._post(url, payload)

    def naver_withhold_return(self, imp_uid, memo, **kwargs):
        url = '{}payments/{}/naver/withhold-return'.format(
            self.imp_url, imp_uid
        )
        payload = {'imp_uid': imp_uid, 'memo': memo}
        if kwargs:
            payload.update(kwargs)
        return self._post(url, payload)

    def naver_resolve_return(self, imp_uid, **kwargs):
        url = '{}payments/{}/naver/resolve-return'.format(
            self.imp_url, imp_uid
        )
        payload = {'imp_uid': imp_uid}
        if kwargs:
            payload.update(kwargs)
        return self._post(url, payload)

    def naver_deposit_point(self, imp_uid):
        url = '{}payments/{}/naver/point'.format(self.imp_url, imp_uid)
        payload = {'imp_uid': imp_uid}
        return self._post(url, payload)

    def naver_confirm(self, imp_uid, **kwargs):
        url = '{}payments/{}/naver/confirm'.format(self.imp_url, imp_uid)
        payload = {'imp_uid': imp_uid}
        if kwargs:
            payload.update(kwargs)
        return self._post(url, payload)

    def naver_product_orders(self, imp_uid):
        url = '{}payments/{}/naver/product-orders'.format(
            self.imp_url, imp_uid
        )
        return self._get(url)

    def naver_single_product_order(self, product_order_id):
        url = '{}naver/product-orders/{}'.format(
            self.imp_url, product_order_id
        )
        return self._get(url)

    def naver_reviews(self, **kwargs):
        url = '{}naver/reviews'.format(self.imp_url)
        for key in ['channel_key', 'from', 'to', 'review_type']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        return self._get(url, kwargs)

    def naver_cash_amount(self, imp_uid):
        url = '{}payments/{}/naver/cash-amount'.format(self.imp_url, imp_uid)
        return self._get(url)

    # ===== Benepia =====

    def benepia_point(self, **kwargs):
        url = '{}benepia/point'.format(self.imp_url)
        for key in ['benepia_user', 'benepia_password', 'channel_key']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        return self._post(url, kwargs)

    def benepia_payment(self, **kwargs):
        url = '{}benepia/payment'.format(self.imp_url)
        for key in [
            'benepia_user', 'benepia_password', 'merchant_uid',
            'amount', 'name', 'channel_key'
        ]:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        return self._post(url, kwargs)

    # ===== CVS =====

    def create_cvs(self, **kwargs):
        url = '{}cvs'.format(self.imp_url)
        for key in ['channel_key', 'merchant_uid', 'amount']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        return self._post(url, kwargs)

    def revoke_cvs(self, imp_uid):
        url = '{}cvs/{}'.format(self.imp_url, imp_uid)
        return self._delete(url)

    # ===== KCP Quick =====

    def kcpquick_delete_member(self, member_id, **kwargs):
        url = '{}kcpquick/members/{}'.format(self.imp_url, member_id)
        for key in ['site_code', 'partner_type', 'partner_subtype']:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        payload = {'member_id': member_id}
        payload.update(kwargs)
        return self._delete(url, payload)

    def kcpquick_payment_money(self, **kwargs):
        url = '{}kcpquick/payment/money'.format(self.imp_url)
        for key in [
            'member_id', 'channel_key', 'merchant_uid',
            'name', 'amount'
        ]:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        return self._post(url, kwargs)

    # ===== Partners =====

    def partner_receipt(self, imp_uid, data):
        url = '{}partners/receipts/{}'.format(self.imp_url, imp_uid)
        payload = {'imp_uid': imp_uid, 'data': data}
        return self._post(url, payload)

    # ===== Payco =====

    def payco_update_order_status(self, imp_uid, status):
        url = '{}payco/orders/status/{}'.format(self.imp_url, imp_uid)
        payload = {'imp_uid': imp_uid, 'status': status}
        return self._post(url, payload)

    # ===== Paymentwall =====

    def paymentwall_delivery(self, **kwargs):
        url = '{}paymentwall/delivery'.format(self.imp_url)
        for key in [
            'imp_uid', 'merchant_uid', 'type', 'status',
            'estimated_delivery_datetime', 'estimated_update_datetime',
            'refundable', 'shipping_address_email'
        ]:
            if key not in kwargs:
                raise KeyError('Essential parameter is missing!: %s' % key)
        return self._post(url, kwargs)

    # ===== Tiers =====

    def find_tier(self, tier_code):
        url = '{}tiers/{}'.format(self.imp_url, tier_code)
        return self._get(url)

    # ===== Users =====

    def find_user_pg(self):
        url = '{}users/pg'.format(self.imp_url)
        return self._get(url)
