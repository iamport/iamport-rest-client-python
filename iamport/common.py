import json
import requests

from iamport.exceptions import ResponseError, HttpError, NeedEssentialParameterException


class _Common:
    def _get_token(self):
        url = '{}users/getToken'.format(self.imp_url)
        payload = {'imp_key': self.imp_key,
                   'imp_secret': self.imp_secret}
        response = self.requests_session.post(
            url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload)
        )
        return self._get_response(response).get('access_token')

    def _get_response(self, response):
        if response.status_code != requests.codes.ok:
            raise HttpError(response.status_code, response.reason)
        result = response.json()
        if result['code'] != 0:
            raise ResponseError(result.get('code'), result.get('message'))
        return result.get('response')

    def _get_headers(self):
        return {'X-ImpTokenHeader': self._get_token()}

    def _get(self, url, payload=None):
        headers = self._get_headers()
        response = self.requests_session.get(url, headers=headers, params=payload)
        return self._get_response(response)

    def _post(self, url, payload=None):
        headers = self._get_headers()
        headers['Content-Type'] = 'application/json'
        response = self.requests_session.post(url, headers=headers, data=json.dumps(payload))
        return self._get_response(response)

    def _delete(self, url):
        headers = self._get_headers()
        response = self.requests_session.delete(url, headers=headers)
        return self._get_response(response)

    def _required_args_check(self, kwargs_set, essential_keys_list):
        for key in essential_keys_list:
            if key not in kwargs_set:
                raise NeedEssentialParameterException(key)

