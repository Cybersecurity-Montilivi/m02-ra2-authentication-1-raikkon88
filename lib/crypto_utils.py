
from jwt import (
    JWT,
    jwk_from_pem,
)
from jwt.utils import get_int_from_datetime
from Crypto.PublicKey import RSA
KEY_FILE = './pk.pem'

def generate_pem_file():
    key = RSA.generate(4096)
    private_key = key.exportKey("PEM")
    fd = open(KEY_FILE, "wb")
    fd.write(private_key)
    fd.close()

def load_signing_key():
    with open(KEY_FILE, 'rb') as fh:
        return jwk_from_pem(fh.read())

def sign_message(message):
    instance = JWT()
    signing_key = load_signing_key()
    return instance.encode(message, signing_key, alg='RS256')