from gregor.consumer import Consumer
from gregor.topic import Topic
from gregor.schema import Schema
from gregor import KafkaClient, registry
from pykafka.common import OffsetType
# Useful logging
import logging
logging.basicConfig(level='DEBUG')

class TestPostTopic(object):
    name = 'test_post2'
    schema = Schema("user.avsc", path='./schemas')

# the following is the BARE MINIMUM needed to build a consumer
class TestPostConsumer(Consumer):
    consumer_group_name = 'test_post'
    topic = TestPostTopic
    zookeeper_connect = '127.0.0.1:2181'
    settings = {
        'auto_offset_reset': OffsetType.LATEST,
    }
    # 'process' receives every message and listens on a loop
    def process(self, message):
        print(message.value)

# you could run the following in a ipython window to deploy manually..
'''
client = KafkaClient(hosts="localhost:9092")
consumer = TestPostConsumer(client)
consumer.consume()
'''