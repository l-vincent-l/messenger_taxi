import falcon, logging, redis, json, requests
from messenger_hook.falcon_messenger import FalconMessenger
from .confirmation import Confirmation
from .sinch import SinchVerif

class M(FalconMessenger, Confirmation):
    def __init__(self, redis_client, sinch, *args, **kwargs):
        self.redis = redis_client
        self.sinch = sinch
        super(M, self).__init__(*args, **kwargs)

    def geo_locate(self, address):
        logging.getLogger('a').error('Requesting BAN to locate address...')
        r = requests.get('http://api-adresse.data.gouv.fr/search/?q={}'.format(address))
        address = r.json()['features'][0]['properties']['label']
        logging.getLogger('a').error('Located {}'.format(address))
        return address

    def transform_message(self, recipient_id, text, attachments):
        logging.getLogger('aa').error('transform_message(%s, %s, %s)'.format(recipient_id, text, attachments))
        # if not self.check_customer_confirmed(recipient_id):
        #     return self.confirm_customer(recipient_id, text)
        id_ = 'localization:{}'.format(recipient_id)
        if not redis_client.exists(id_):
            redis_client.set(id_, 'location_asked')
            return 'À quelle adresse souhaitez-vous un prendre un taxi ?'
        else:
            if text:
                logging.getLogger('a').error('text: {}'.format(text))
                return self.geo_locate(text)
            elif attachments:
                # Position
                logging.getLogger('a').error('attachments: {}'.format(attachments))
                return 'got attachments'
            return 'got nothing'



app = falcon.API()
redis_client = redis.Redis()
sinch = SinchVerif(config['sinch_key'], config['sinch_secret'])

with open('/srv/www/taxi/taxi/config.json', encoding='utf-8') as f:
    config = json.load(f)

messenger = M(redis_client, sinch, config['verify'], config['messenger_key'])

app.add_route('/taxi/verify/', messenger)

