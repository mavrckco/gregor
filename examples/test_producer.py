from gregor.producer import Producer
from gregor.topic import Topic
from gregor.schema import Schema
from gregor import KafkaClient, registry


class TestPostTopic(object):
    name = 'test_post'
    schema = Schema("user.avsc", path='./schemas')

class TestPostProducer(Producer):
    topic = TestPostTopic

client = KafkaClient(hosts="127.0.0.1:9092")

# Create the Producer
prod = TestPostProducer(client, min_queued_messages=0)

# Sample Dataset
post = {"id":1,"first_name":"jack","last_name":"johnson","age":5}

# Send test_consumer
prod.produce(post)