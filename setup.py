from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

install_requires=[
    'pykafka==2.1.1',
    'avro-python3==1.8.1'
]

tests_require = [
    'pytest>=2.8.0',
    'pytest-mock',
    'testinstances'
]


setup(name='gregor',
      version='0.2',
      description='High level Kafka module wrapped around the pykafka library https://github.com/Parsely/pykafka that enforces Kafka best practices and encourages code reusability.',
      url='https://bitbucket.org/mavrck/gregor',
      author='Mike Laderman',
      author_email='mike@mavrck.co',
      license='MIT',
      packages=['gregor'],
      install_requires=install_requires,
      tests_require=tests_require,
      cmdclass={'test': PyTest},
      scripts=['bin/run_consumer.py'],
      zip_safe=False)
