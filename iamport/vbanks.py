from iamport.common import _Common


class Vbanks(_Common):
    def revoke_vbank_by_imp_uid(self, imp_uid):
        url = '{}vbanks/{}'.format(self.imp_url, imp_uid)
        return self._delete(url)

