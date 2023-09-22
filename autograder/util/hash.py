import hashlib

DEFAULT_ENCODING = 'utf8'

def sha256_hex(payload, encoding = DEFAULT_ENCODING):
    digest = hashlib.new('sha256')
    digest.update(payload.encode(encoding))
    return digest.hexdigest()
