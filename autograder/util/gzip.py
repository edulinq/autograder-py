import gzip
import base64

DEFAULT_ENCODING = 'utf-8'

def from_base64(contents, encoding = DEFAULT_ENCODING, **kwargs):
    contents = base64.b64decode(contents.encode(encoding), validate = True)
    return from_bytes(contents, encoding = encoding, **kwargs)

def from_bytes(content, string = False, encoding = DEFAULT_ENCODING):
    data = gzip.decompress(content)

    if (not string):
        return data

    return data.decode(encoding)

def to_base64(path, encoding = DEFAULT_ENCODING):
    data = to_bytes(path)
    content = base64.b64encode(data)
    return content.decode(encoding)

def to_bytes(path):
    with open(path, 'rb') as file:
        data = file.read()

    return gzip.compress(data)
