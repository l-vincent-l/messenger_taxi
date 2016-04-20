from .tasks import verify_phone_number
import logging

class Confirmation:
    def check_customer_confirmed(self, recipient_id):
        return self.redis.sismember('customers_confirmed', recipient_id)

    def confirm_customer(self, recipient_id, text):
        id_ = 'confirmation:{}'.format(recipient_id)
        if not self.redis.exists(id_):
            self.redis.set(id_, 'phone_number_asked')
            return 'Pour commencer, entrez votre numéro de téléphone'
        status = self.redis.get(id_).decode('utf-8')
        if status == 'phone_number_asked':
            self.redis.set('phone_number:{}'.format(recipient_id), text)
            self.redis.set(id_, 'sms_sent')
            self.sinch.send_verification(text)
            return 'Nous vous avons envoyé un sms au {}'.format(text)
        if status == 'sms_sent':
            phone_number = self.redis.get('phone_number:{}'.format(recipient_id)).decode('utf-8')
            if self.sinch.confirm_code(text, phone_number):
                self.redis.sadd('customers_confirmed', recipient_id)
                return "Ok, j'ai votre numéro, à quelle adresse voulez vous le taxi ?"
            return 'Mauvais numéro'

