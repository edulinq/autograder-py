import gzip
import base64

DEFAULT_ENCODING = 'utf-8'

def from_base64(contents, encoding = DEFAULT_ENCODING, **kwargs):
    contents = base64.b64decode(contents.encode(encoding), validate = True)
    return from_bytes(contents, encoding = encoding, **kwargs)

def from_bytes(content, string = True, encoding = DEFAULT_ENCODING):
    data = gzip.decompress(content)

    if (not string):
        return data

    return data.decode(encoding)
