from gregor import Producer, Consumer
from .topics import UserTopic
import pytest

class UserProducer(Producer):
    topic = UserTopic

class UserConsumer(Consumer):
    topic = UserTopic
    consumer_group_name = 'test-user'
    settings = {
        'consumer_timeout_ms': 1000
    }

    def process(self, message):
        self.data = message.value
        self.consumer.stop()

class TestProducer(object):

    def test_arguments_passed_on(self, kafka_client, mocker):
        max_queued_messages = 1
        min_queued_messages = 1
        sync = True

        producer = UserProducer(kafka_client, max_queued_messages=max_queued_messages, min_queued_messages=min_queued_messages, sync=sync)
        assert producer.producer._min_queued_messages == min_queued_messages
        assert producer.producer._max_queued_messages == max_queued_messages
        assert producer.producer._synchronous == sync

    def test_produce_valid_message(self, kafka_client):
        user = {
            'id': 1,
            'first_name': 'Gregor',
            'last_name': 'Samsa',
            'age': 30
        }
        consumer = UserConsumer(kafka_client)
        producer = UserProducer(kafka_client, max_queued_messages=1, min_queued_messages=1, sync=True)
        producer.produce(user)
        try:
            consumer.consume()
        except:
            pass
        finally:
            assert consumer.data == user

    def test_produce_invalid_message_fail(self, mocker):
        invalid_user = {
            'bad_field': 'terrible'
        }
        producer = UserProducer(mocker.MagicMock(), max_queued_messages=1, min_queued_messages=1, sync=True)
        with pytest.raises(ValueError, message="Raises a ValueError for an invalid message."):
            producer.produce(invalid_user)

    def test_requires_topic(self, mocker):
        with pytest.raises(AttributeError, message="Raises an AttributeError if no topic is assigned."):
            Producer(mocker.MagicMock(), max_queued_messages=1, min_queued_messages=1, sync=True)
