# -*- coding: utf-8 -*-
import requests

from iamport.certifications import Certifications
from iamport.payments import Payments
from iamport.subscribe import Subscribe
from iamport.subscribe_customers import Subscribe_customers
from iamport.vbanks import Vbanks

__all__ = ['IAMPORT_API_URL', 'Iamport']
IAMPORT_API_URL = 'https://api.iamport.kr/'


class Iamport(Certifications, Payments, Subscribe, Vbanks, Subscribe_customers):
    def __init__(self, imp_key, imp_secret, imp_url=IAMPORT_API_URL):
        self.imp_key = imp_key
        self.imp_secret = imp_secret
        self.imp_url = imp_url
        requests_session = requests.Session()
        requests_adapters = requests.adapters.HTTPAdapter(max_retries=3)
        requests_session.mount('https://', requests_adapters)
        self.requests_session = requests_session

