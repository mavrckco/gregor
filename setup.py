from setuptools import setup

setup(name='gregor',
      version='0.1',
      description='High level Kafka module wrapped around the pykafka library https://github.com/Parsely/pykafka that enforces Kafka best practices and encourages code reusability.',
      url='https://bitbucket.org/mavrck/gregor',
      author='Mike Laderman',
      author_email='mike@mavrck.co',
      license='MIT',
      packages=['gregor'],
      install_requires=[
          'pykafka==2.1.1',
          'avro==1.7.7'
      ],
      zip_safe=False)
