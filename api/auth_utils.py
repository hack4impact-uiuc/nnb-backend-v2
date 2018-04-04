import hashlib
import secrets
import string

HASH_ALGORITHM = 'sha256'
NUM_HASH_ITERATIONS = 100000
HASH_OUTPUT_LEN = 32

SALT_NUM_BYTES = 32

MIN_REQUIRED_PASSWORD_LEN = 7

def hash_password(password, salt):
    password_bytes = bytearray(password, encoding='utf-8')
    salt_bytes = bytes.fromhex(salt)
    dk = hashlib.pbkdf2_hmac(HASH_ALGORITHM, password_bytes, salt_bytes,
                                NUM_HASH_ITERATIONS, HASH_OUTPUT_LEN)
    return dk.hex()

def generate_salt():
    return secrets.token_hex(SALT_NUM_BYTES)

def validate_password_requirements(password):
    failure_message = []

    if len(password) < MIN_REQUIRED_PASSWORD_LEN:
        failure_message.append('password must be at least {} characters long'\
                .format(MIN_REQUIRED_PASSWORD_LEN))
    
    return '\n'.join(failure_message)
