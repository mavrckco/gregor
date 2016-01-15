from gregor.consumer import Consumer
from gregor.topic import Topic
from gregor.schema import Schema
from gregor import KafkaClient, registry
from pykafka.common import OffsetType


class TestPostTopic(object):
    name = 'test_post'
    schema = Schema("user.avsc", path='./schemas')

class TestPostConsumer(Consumer):
    consumer_group_name = 'facebook_post'
    topic = TestPostTopic

    settings = {
        'auto_offset_reset': OffsetType.LATEST

    }
    # 'process' receives every message and listens on a loop
    def process(self, message):
        print(message.value)

# default host is ussually 127.0.0.1:9092
client = KafkaClient(hosts="127.0.0.1:9092")
consumer = TestPostConsumer(client)
consumer.consume()
