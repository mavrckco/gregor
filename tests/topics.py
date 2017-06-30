from gregor import Topic, Schema
import os

PATH = os.path.join(os.path.dirname(__file__), 'schemas')

class UserTopic(Topic):
    name = 'test_user'
    schema = Schema('user.avsc', path=PATH)
