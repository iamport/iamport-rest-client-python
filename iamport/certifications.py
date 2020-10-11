from iamport.common import _Common


class Certifications(_Common):
    def find_certification(self, imp_uid):
        url = '{}certifications/{}'.format(self.imp_url, imp_uid)
        return self._get(url)

    def cancel_certification(self, imp_uid):
        url = '{}certifications/{}'.format(self.imp_url, imp_uid)
        return self._delete(url)

