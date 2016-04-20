from .tasks import verify_phone_number

class Confirmation:
    def check_customer_confirmed(self, recipient_id):
        return self.redis.sismember('customers_confirmed', recipient_id)

    def confirm_customer(self, recipient_id, text):
        id_ = 'confirmation:{}'.format(recipient_id)
        if not redis.exists(id_):
            redis.set(id_, 'phone_number_asked')
            return 'Pour commencer, entrez votre numéro de téléphone'
        status = redis.get(id_, 'phone_number_asked') 
        if status == 'phone_number_asked':
            verify_phone_number.delay(recipiend_id, text)
            
