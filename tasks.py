from celery import Celery
import sinch, redis


with open('config.json', encoding='utf-8') as f:
    config = json.load('config.json')
sinch = sinchsms.SinchSMS(config['sinch_key'], config['sinch_secret'])
sinch.SEND_SMS_URL = 'https://sandbox.sinch.com/v1/sms/'
sinch.CHECK_STATUS_URL = 'https://sandbox.sinch.com/v1/sms/'

redis_client = redis.Redis()


app = Celery('tasks', broker='redis://localhost//')

@app.task
def verify_phone_number(recipient_id, phone_number):
    sinch.send_message(recipient_id, 'Code de confirmation blablataxi')
    redis.set('confirmation:{}'.format(recipient_id), 'sms_sent')
    update_sms_status.apply_async(recipient_id, phone_number, countdown=1)
    
@app.task
def update_sms_status(recipient_id, phone_number):
    status = sinch.check_status(phone_number)
    if status == 'Successful':
        redis.set('confirmation:{}'.format(recipient_id), 'successful')
        redis.sset('customers_confirmed', recipient_id)
    else:
        update_sms_status.apply_async(recipient_id, phone_number, countdown=1)

