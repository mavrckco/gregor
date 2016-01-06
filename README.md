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