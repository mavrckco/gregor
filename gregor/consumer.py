from .register import RegisteredMetaclass
import time
from pykafka.exceptions import ConsumerStoppedException

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
                if hasattr(self.topic, 'schema'):
                    message.value = self.topic.schema.decode(message.value)
                else:
                    message.value = message.value.decode()
            except ValueError as e:
                print(e)
            else:
                self.process(message)

    def process(self, message):
        raise NotImplementedError("You must implement a process function.")


class BatchConsumer(Consumer):
    """
        Kafka Consumer with helpers to handle batches of methods. This is useful
        for sending larger amounts of data to bulk analyzers, and for doing
        bulk database inserts.

        Args:
            client (pykafka.KafkaClient): A client to connect to Kafka.
            max_batch_size (int): The maximum number of messages that can be held in a batch before processing.
            max_batch_idle_seconds (int): The number of seconds before forcing processing a batch.
    """

    max_batch_size = 100
    max_batch_idle_seconds = 15

    def __init__(self, client, *args, **kwargs):

        if not self.max_batch_size:
            raise ValueError("max_batch_size must be defined")     
        if not self.max_batch_idle_seconds:
            raise ValueError("max_batch_idle_seconds must be defined")            

        self._batch_offset = None
        self._batch_messages = []
        self._last_commited_time = time.time()

        super().__init__(client, *args, **kwargs)
        self._settings.update({'post_rebalance_callback': self.post_rebalance_callback})
        if self.max_batch_idle_seconds:
            self._settings.update({'consumer_timeout_ms': self.max_batch_idle_seconds * 1000})

    def post_rebalance_callback(self, consumer, old_offsets, new_offsets):
        """
            Makes sure that on a rebalance (a worker joins or leaves the existing
            consumer group), that the worker flushes out and commits its work before
            letting the other worker start consuming messages. Also makes sure
            that the internal partition offsets get set properly to avoid duplicate
            messages coming through. There were cases in which the new_offset already
            included messages from the old_offset. Exactly once delivery is NOT guaranteed,
            but at this stage it's an edge case.
        """
        if not old_offsets:
            return

        # check that the new_partition doesn't ingest messages already handled by
        # the old batch
        updated = False
        for partition, new_offset in new_offsets.items():
            old_offset = old_offsets.get(partition)
            if old_offset and old_offset > new_offset:
                new_offsets[partition] = old_offsets[partition]
                updated = True

        # flush out current batch
        self.process_batch(self.batch_messages)
        self._reset_batch(new_offsets=new_offsets)

        # if the offsets had to be updated, then return
        # the corrected new_offsets so that the consumer
        # will rebalance itself
        if updated:
            return new_offsets    

    def consume(self):
        """
            Loops through messages from the consumer and processes
            them in batches.
        """
        while True:
            super().consume()
            # if super().consume ends (no more messages within timeout)
            # then we want to process the current data we have and then reset
            # the batch, and attempt to consume again.
            self.process_batch(self.batch_messages)
            self._reset_batch()


    def _reset_batch(self, new_offsets=None):
        """
            Resets the state on the worker after processing a batch.
        """
        if self.consumer._running:
            # commit offsets to the worker to show that the work has been done
            self.consumer.commit_offsets()
            # keep track of the last commited time for the worker flush
            self._last_commited_time = time.time()
        self._batch_offset = new_offsets or (self.consumer.held_offsets.copy() if self.consumer.held_offsets else None)
        self._batch_messages = []

    @property
    def batch_messages(self):
        """
            An array of the batch messages that have yet to be processed.
        """
        return getattr(self, '_batch_messages', [])

    @property
    def batch_offset(self):
        """
            Partition offsets at the time of the start of the batch.
        """
        return self._batch_offset

    @batch_offset.setter
    def batch_offset(self, offset):
        """
            Partition offsets at the time of the start of the batch.
        """        
        self._batch_offset = offset

    def process(self, message):
        """
            Special process method for managing batches.
        """

        # add message to list of messages to be processed
        if message is not None:
            self._batch_messages.append(message)

        # if we have reached our batch capacity, or we've reached our time limit
        # to handle a batch, process the batch.
        if (len(self.batch_messages) >= self.max_batch_size) or (time.time() - self._last_commited_time >= self.max_batch_idle_seconds):
            self.process_batch(self.batch_messages)
            self._reset_batch()

    def process_batch(self, messages):
        """
            Main logic for batch processing goes here. Messages is the
            list of messages added from the process() method. 
        """
        raise NotImplementedError