class Producer(object):
    topic = None

    def __init__(self, client, topic=None, **kwargs):
        self._options = kwargs
        self._client = client
        if not self.topic:
            if topic:
                self.topic = topic
            else:
                raise "You must assign a valid topic to this producer."
        self._producer = None

    @property
    def producer(self):
        if not self._producer:
            topic_instance = self._client.topics[self.topic.name.encode()]
            self._producer = topic_instance.get_producer(**self._options)
        return self._producer

    def produce(self, message):
        try:
            encoded_message = self.topic.schema.encode(message)
        except ValueError as error:
            raise error
        else:
            self.producer.produce(encoded_message)
