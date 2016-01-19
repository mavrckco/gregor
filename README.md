Gregor
=======


Gregor is a high level wrapper around PyKafka, which is a Kafka 0.8.2 protocol client for Python. It includes class based consumer and producers, along with utilities to launch consumer worker instances. It runs under Python 3.4+.


Gregor's primary goal is to provide a simple and reusable structure for generating python based producers and consumers. 

You can install Gregor from Bitbucket with


    $ pip3 install git+https://bitbucket.com/mavrck/gregor.git


You can install Gregor for local development and testing with


    $ python setup.py develop

JVM Kafka client: https://github.com/apache/kafka/tree/0.8.2/clients/src/main/java/org/apache/kafka

PyKafka: http://pykafka.readthedocs.org/en/latest/

Getting Started
---------------

Assuming you have a Kafka instance running on localhost, you can use PyKafka
to connect to it.


Schemas
----
Gregor forces the use of [Avro](https://avro.apache.org/docs/current/) schemas to ensure that all data sent is serialized in the correct format, so that downstream consumers have a guarantee that the data they receive is in the expected format.

We recommend that you create a directory in your application to store all schemas. Here is an example to create your first schema. Avro schemas should be saved with the .avsc extension.

Here is an example user schema stored in schemas/user.avsc.

```
#!json
{
    "namespace": "user.avro",
    "type": "record",
    "name": "User",
    "fields": [
        {"name": "id", "type": "int", "doc": "The id of the user."},
        {"name": "first_name", "type": "string", "doc": "The user's first name."},
        {"name": "last_name", "type": "string", "doc": "The user's last name."},
        {"name": "age", "type": "int", "doc": "The user's age."}
    ]
}
```
To utilize the schema, you must create a topic, and generate an instance of this schema that can encode and decode data to and from kafka on class declaration. Path defaults to the current directory.

```
#!python

from gregor import Topic
from gregor import Schema

class UserTopic(Topic):
    name = 'user'
    schema = Schema("user.avsc", path='./schemas')

```

After creating a topic, we can now generate Producers and Consumers.

Running The Examples
---
* cd in `examples`
* Turn on Kafka 
* Turn on ZooKeeper
* Turn on the consumer in a separate shell
    * `python3.5 test_consumer.py`
* Turn on the producer in a separate shell
    * `python3.5 test_producer.py`
* Running the consumer console command
    * `run_consumer.py -n 'test_print_consumer.TestPostConsumer' --hosts 127.0.0.1:9092 --root ./mavrck`

Diving Deep Into The Codebase
---
* Building a Producer
    * view the example and for details on passing options read up on the following
    * [Producer Init Parameters](https://github.com/Parsely/pykafka/blob/master/pykafka/producer.py#L47)
* Building a Consumer
    * view the example and for details on passing options read up on the following
    * [Consumer Init Parameters](https://github.com/Parsely/pykafka/blob/master/pykafka/balancedconsumer.py#L59)

Trouble Shooting
---

* Creating a Topic in Zookeeper (**if auto create topic fails**)
    * `kafka-topics.sh --create --zookeeper 172.16.0.4:2181 --replication-factor 1 --partitions 1 --topic **test_post**`
* Debugging Schema Errors from AVRO
    * **TO DO**