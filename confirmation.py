from .tasks import verify_phone_number

class Confirmation:
    def check_customer_confirmed(self, recipient_id):
        return self.redis.sismember('customers_confirmed', recipient_id)

    def confirm_customer(self, recipient_id, text):
        id_ = 'confirmation:{}'.format(recipient_id)
        if not redis.exists(id_):
            self.redis.set(id_, 'phone_number_asked')
            return 'Pour commencer, entrez votre numéro de téléphone'
        status = self.redis.get(id_, 'phone_number_asked') 
        if status == 'phone_number_asked':
            self.redis.set('phone_number:{}'.format(recipient_id), text)
            verify_phone_number.delay(recipient_id, text)
        if status == 'sms_sent':
            phone_number = self.redis.get('phone_number:{}'.format(recipient_id))
            if self.sinch.confirm_code(text, phone_number):
                self.redis.sset('customer_confirmed', phone_number)
                return "Ok, j'ai votre numéro, à quelle adresse voulez vous le taxi ?"

