import secrets

import argon2.low_level

DEFAULT_PASSWORD_LEN = 32
SALT_LENGTH_BYTES = 16

ARGON2_KEY_LEN_BYTES = 32
ARGON2_MEM_KB = 64 * 1024
ARGON2_THREADS = 4
ARGON2_TIME = 1

ENCODING = 'utf-8'

def rand_pass():
    return rand_bytes(DEFAULT_PASSWORD_LEN // 2).hex()

def rand_bytes(length):
    return secrets.token_bytes(length)

def hash(password):
    salt = rand_bytes(SALT_LENGTH_BYTES)

    hashpass = argon2.low_level.hash_secret_raw(
        password.encode(ENCODING), salt,
        time_cost = ARGON2_TIME, memory_cost = ARGON2_MEM_KB,
        parallelism = ARGON2_THREADS, hash_len = ARGON2_KEY_LEN_BYTES,
        type = argon2.low_level.Type.ID)

    return hashpass.hex(), salt.hex()
