
from jwt import (
    JWT,
    jwk_from_pem,
)
from jwt.utils import get_int_from_datetime
from Crypto.PublicKey import RSA

SIGNING_KEY_FILE = './sk.pem'
VERIFING_KEY_FILE = './vk.pem'

def save_key(file, key):
    fd = open(file, "wb")
    fd.write(key)
    fd.close()

def generate_pem_file():
    key = RSA.generate(4096)
    private_key = key.exportKey("PEM")
    public_key = key.publickey().exportKey("PEM")
    save_key(SIGNING_KEY_FILE, private_key)
    save_key(VERIFING_KEY_FILE, public_key)

def load_signing_key():
    with open(SIGNING_KEY_FILE, 'rb') as fh:
        return jwk_from_pem(fh.read())

def load_verifing_key(): 
    with open(VERIFING_KEY_FILE, 'rb') as fh:
        return jwk_from_pem(fh.read())

def sign_message(message):
    instance = JWT()
    signing_key = load_signing_key()
    return instance.encode(message, signing_key, alg='RS256')

def verify_message(token):
    instance = JWT()
    verifying_key = load_verifing_key()
    return instance.decode(token, verifying_key, do_time_check=True)