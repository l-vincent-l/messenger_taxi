import sinchsms

class SinchVerif(sinchsms.SinchSMS):
    sinch.SEND_SMS_URL = 'https://sandbox.sinch.com/v1/sms/'
    sinch.CHECK_STATUS_URL = 'https://sandbox.sinch.com/v1/sms/'
    sinch.VERIFICATION_URL = 'https://sandbox.sinch.com/v1/verifications/'

    def _request(self, url, values=None, method=None):
        """ Send a request and read response.
            Sends a get request if values are None, post request otherwise.
        """
        if values:
            json_data = json.dumps(values)
            request = urllib2.Request(url, json_data.encode())
            request.add_header('content-type', 'application/json')
            request.add_header('authorization', self._auth)
            if method:
                request.get_method = lambda: 'PUT'
            connection = urllib2.urlopen(request)
            response = connection.read()
            connection.close()
        else:
            request = urllib2.Request(url)
            request.add_header('authorization', self._auth)
            connection = urllib2.urlopen(request)
            response = connection.read()
            connection.close()

        try:
            result = json.loads(response.decode())
        except ValueError as exception:
            return {'errorCode': 1, 'message': str(exception)}

        return result

    def send_verification(self, phone_number):
        self._request(self.VERIFICATION_URL, {
            "identity": { "type":"number", "endpoint":phone_number},
            "method": "sms"
            })

    def confirm_code(self, code, phone_number):
        response = self._request(self.VERIFICATION_URL+'sms/{}'.format(phone_number),
                {"method": "sms", "sms":{"code": code}}, 'PUT')
        return response['status'] == 'SUCCESSFUL'
