import sinchsms, json, requests, logging

class SinchVerif(sinchsms.SinchSMS):
    SEND_SMS_URL = 'https://api.sinch.com/v1/sms/'
    CHECK_STATUS_URL = 'https://api.sinch.com/v1/sms/'
    VERIFICATION_URL = 'https://api.sinch.com/verification/v1/verifications'

    def _request(self, url, values=None, method='POST'):
        """ Send a request and read response.
            Sends a get request if values are None, post request otherwise.
        """
        headers = {'authorization': self._auth}
        logging.getLogger('aa').error(headers)
        if values:
            headers['accept'] = 'application/json'
            method = requests.post if method == 'POST' else requests.put
            request = method(url, json=values, headers=headers)
        else:
            request = requests.get(url, headers=headers)
        try:
            result = request.json()
        except ValueError as exception:
            return {'errorCode': 1, 'message': str(exception)}

        return result

    def send_verification(self, phone_number):
        result = self._request(self.VERIFICATION_URL, {
            "identity": { "type":"number", "endpoint":phone_number},
            "method": "sms"
            })

    def confirm_code(self, code, phone_number):
        response = self._request(self.VERIFICATION_URL+'/number/{}'.format(phone_number),
                {"method": "sms", "sms":{"code": code}}, 'PUT')
        return response.get('status') == 'SUCCESSFUL'
