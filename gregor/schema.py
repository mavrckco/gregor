import os
import avro.schema
import io
from avro.io import DatumWriter, DatumReader, AvroTypeException

class Schema(object):

    def __init__(self, schema_name, path='.', *args, **kwargs):
        self.schema_file_name = os.path.join(path, schema_name)
        self._schema = None
        self._writer = None
        self._reader = None

    @property
    def schema(self):
        if not self._schema:
            schema_file = self.schema_file_name
            with open(schema_file) as f:
                schema = avro.schema.Parse(f.read()) 
            return schema
        return self._schema

    @property
    def writer(self):
        if not self._writer:
            writer = DatumWriter(writer_schema=self.schema) 
            self._bytes_writer = io.BytesIO()
            self._encoder = avro.io.BinaryEncoder(self._bytes_writer)
            return writer
        return self._writer

    @property
    def reader(self):
        if not self._reader:
            reader = DatumReader(self.schema) 
            self._bytes_reader = io.BytesIO()
            self._decoder = avro.io.BinaryDecoder(self._bytes_reader)
            return reader
        return self._reader 
    
    def encode(self, message):
        try:
            self.writer.write(message, self._encoder)
        except AvroTypeException as e:
            raise ValueError("{} does not match the schema {}".format(e.args[0], self.schema_file_name))
        else:
            raw = self._bytes_writer.getvalue()
            return raw

    def decode(self, message):
        bytes_reader = io.BytesIO(message)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        value = self.reader.read(decoder)
        return value
