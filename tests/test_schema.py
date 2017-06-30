from gregor import Schema
from .topics import UserTopic
import os
import avro
import pytest
import sys

PATH = os.path.join(os.path.dirname(__file__), 'schemas')

class TestSchema(object):

    def test_init_valid_file(self):
        filename = 'user.avsc'
        schema = Schema(filename, path=PATH)
        assert schema.schema.name == 'User'

    def test_init_incorrect_path(self):
        filename = 'fake.avsc'
        schema = Schema(filename, path=PATH)
        with pytest.raises(FileNotFoundError, message="Raises a FileNotFoundError if schema does not exist."):
            assert schema.schema

    def test_invalid_schema(self):
        filename = 'bad_schema.avsc'
        schema = Schema(filename, path=PATH)
        with pytest.raises(avro.schema.SchemaParseException, message="Raises a SchemaParseException if schema is invalid."):
            assert schema.schema

    def test_decode_encode_valid(self):
        filename = 'user.avsc'
        schema = Schema(filename, path=PATH)
        user = {
            'id': 1,
            'first_name': 'Gregor',
            'last_name': 'Samsa',
            'age': 30
        }
        encoded = schema.encode(user)
        assert isinstance(encoded, bytes)

        decoded = schema.decode(encoded)
        assert decoded == user

    def test_encode_invalid(self):
        filename = 'user.avsc'
        schema = Schema(filename, path=PATH)
        user = {
            'bad': 'bad!'
        }
        with pytest.raises(ValueError, message="Raises a ValueError if data is invalid."):
            encoded = schema.encode(user)
