#!/usr/bin/python3

import argparse
import importlib
import os
import sys
import time
import signal
from gregor import registry
from pykafka import KafkaClient

def main(class_name, hosts):
    consumer_class = registry.get(class_name)
    if not consumer_class:
        raise ValueError("{} is not a registered consumer.".format(class_name))
    client = KafkaClient(hosts=','.join(hosts))
    consumer = consumer_class(client)
    try:
        consumer.consume()
    except Exception as e:
        print(e)
        sys.exit(0)

def exit_handler(signum, frame):
    print('\rexiting...')
    sys.exit(0)


while __name__ == '__main__':
    try:
        # Register keyboard interrupt handler
        signal.signal(signal.SIGINT, exit_handler)

        # command line parsers
        parser = argparse.ArgumentParser(description='Run an instance of a kafka consumer.')
        parser.add_argument('-n', '--name', type=str, help='File and Class to be run i.e. my_consumer.MyConsumer', required=True)
        parser.add_argument('--hosts', type=str, nargs='+', help='List of kafka hosts to connect the consumer to.', required=False, default=['127.0.0.1:9092'])
        parser.add_argument('--root', type=str, help='Root Path of where the consumer is being run', required=False, default='.')
        args = parser.parse_args()

        # load module
        module, consumer_name = args.name.split('.')
        hosts = args.hosts
        root = args.root
        try:
            importlib.machinery.SourceFileLoader(module, os.path.join(root, '{}.py'.format(module))).load_module()
        except ImportError as error:
            raise error
        else:
            main(consumer_name, hosts)
    except OSError as e:
        print('Consumer Crashed with error {}'.format(e))
        time.sleep(5)


