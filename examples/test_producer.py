from gregor.producer import Producer
from gregor.topic import Topic
from gregor.schema import Schema
from gregor import KafkaClient, registry
# Useful logging
import logging
logging.basicConfig(level='DEBUG')

class TestPostTopic(object):
    name = 'test_post'
    schema = Schema("user.avsc", path='./schemas')

class TestPostProducer(Producer):
    topic = TestPostTopic

client = KafkaClient(hosts="localhost:9092")

# Create the Producer, pass pykafka producer options below
# https://github.com/Parsely/pykafka/blob/master/pykafka/producer.py#L47
prod = TestPostProducer(client, max_queued_messages=1 ,min_queued_messages=1)

# Sample Dataset
post = {"id":1,"first_name":"jack","last_name":"johnson","age":5}

# Send to test_consumer 3 times
prod.produce(post)
prod.produce(post)
prod.produce(post)
print("ok!")