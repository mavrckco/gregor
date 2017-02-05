import pytest

from pykafka.test.utils import get_cluster, stop_cluster
from pykafka import KafkaClient


@pytest.fixture(scope='session')
def kafka(request):
    cluster = get_cluster()

    def teardown():
        stop_cluster(cluster)

    request.addfinalizer(teardown)
    return cluster

@pytest.fixture(scope='function')
def kafka_client(request, kafka):
    client = KafkaClient(hosts=kafka.brokers)

    # for topic in available_topics:
        # kafka.create_topic(topic.name, 3, 1)
    kafka.create_topic('test_user', 3, 1)

    def teardown():
        kafka.connection.flush()

    request.addfinalizer(teardown)
    return client
