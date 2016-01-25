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
                self._schema = avro.schema.Parse(f.read()) 
        return self._schema

    @property
    def writer(self):
        if not self._writer:
            # set up the writer, byte stream, and encoder for writing data
            self._writer = DatumWriter(writer_schema=self.schema)
            self._bytes_writer = io.BytesIO()
            self._encoder = avro.io.BinaryEncoder(self._bytes_writer)
        return self._writer

    @property
    def reader(self):
        if not self._reader:
            self._reader = DatumReader(self.schema) 
            self._bytes_reader = io.BytesIO()
            self._decoder = avro.io.BinaryDecoder(self._bytes_reader)
        return self._reader 
    
    def encode(self, message):
        try:
            # write a message to the internal byte stream through the avro encoder
            self.writer.write(message, self._encoder)
        except AvroTypeException as e:
            raise ValueError("{} does not match the schema {}".format(e.args[0], self.schema_file_name))
        else:
            # fetch the raw bytes value
            raw = self._bytes_writer.getvalue()

            # reset the byte stream so we can reuse it
            self._bytes_writer.seek(0)
            self._bytes_writer.truncate(0)
            return raw

    def decode(self, message):
        bytes_reader = io.BytesIO(message)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        value = self.reader.read(decoder)
        return value
