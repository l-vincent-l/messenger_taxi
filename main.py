import falcon, logging, redis
from messenger_hook.falcon_messenger import FalconMessenger
from .confirmation import Confirmation

class M(FalconMessenger, Confirmation):
    def __init__(self, redis_client, *args, **kwargs):
        self.redis = redis_client
        super(M, self).__init__(*args, **kwargs)
        

    def transform_message(self, recipient_id, text, attachments):
        logging.getLogger('aa').error('transform_message(%s, %s, %s)'.format(recipient_id, text, attachments))
        if not self.check_customer_confirmed(recipient_id):
            return self.confirm_customer(recipient_id, text)
        if text:
            logging.getLogger('a').error('text: {}'.format(text))
            return 'got text'
        elif attachments:
            logging.getLogger('a').error('attachments: {}'.format(attachments))
            return 'got attachments'
        return 'got nothing'


app = falcon.API()
redis_client = redis.Redis()
with open('config.json', encoding='utf-8') as f:
    config = json.load('config.json')

messenger = M(redis_client, config['verify'], config['messenger_key'])

app.add_route('/taxi/verify/', messenger)

