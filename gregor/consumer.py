from .register import RegisteredMetaclass

class Consumer(object, metaclass=RegisteredMetaclass):
    topic = None
    consumer_group_name = None
    settings = {}

    def __init__(self, client, *args, **kwargs):
        self._client = client
        if not self.topic:
            raise AttributeError("You must assign a topic to this consumer.")
        if not self.consumer_group_name:
            raise AttributeError("You must assign a consumer_group_name to this consumer.")
        self._topic = client.topics[self.topic.name.encode()]
        self._consumer = None
        self._settings = {}
        self._settings.update(self.settings)

    @property
    def consumer(self):
        if not self._consumer:
            topic_instance = self._client.topics[self.topic.name.encode()]
            self._consumer = topic_instance.get_balanced_consumer(consumer_group=self.consumer_group_name.encode(), **self._settings)
        return self._consumer

    def consume(self):
        for message in self.consumer:
            try:
                message.value = self.topic.schema.decode(message.value)
            except ValueError as e:
                print(e)
            else:
                self.process(message)

    def process(self, message):
        raise NotImplementedError("You must implement a process function.")