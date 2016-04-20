from celery import Celery
import redis, json
from .sinch import SinchVerif


with open('/srv/www/taxi/taxi/config.json', encoding='utf-8') as f:
    config = json.load(f)
sinch = SinchVerif(config['sinch_key'], config['sinch_secret'])

redis_client = redis.Redis()


app = Celery('tasks', broker='redis://localhost//')

@app.task
def verify_phone_number(recipient_id, phone_number):
    sinch.send_verification(recipient_id, 'Code de confirmation blablataxi')
    redis.set('confirmation:{}'.format(recipient_id), 'sms_sent')
