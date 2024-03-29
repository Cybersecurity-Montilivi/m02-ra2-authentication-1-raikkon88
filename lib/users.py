import secrets
from hashlib import pbkdf2_hmac
from datetime import datetime, timedelta, timezone
from jwt.utils import get_int_from_datetime
from .crypto_utils import (sign_message, verify_message)

REGISTER_TOKEN_LENGTH = 64
ITERATIONS = 500000

class Users:

    def __init__(self, db):
        self.db = db

    def generate_hash(self, salt, password):
        dk = pbkdf2_hmac('sha3_512', bytes(password, 'utf-8'), bytes(salt, 'utf-8')*2, ITERATIONS)
        return dk.hex()

    def register(self, email):
        existing_user = self.db.get_user_by_email(email)
        if existing_user != None:
            raise Exception("The user already exists")
        user = {"email": email, "token": secrets.token_urlsafe(
            REGISTER_TOKEN_LENGTH)}
        self.db.set_user(user)
        return user

    def init(self, token, password):
        existing_user = self.db.get_user_by_token(token)
        if existing_user == None:
            raise Exception("The user does not exist")
        existing_user['salt'] = secrets.token_hex(16)
        existing_user['hash'] = self.generate_hash(existing_user["salt"], password)
        existing_user['token'] = None

    def login(self, email, password): 
        existing_user = self.db.get_user_by_email(email)
        if existing_user == None:
            raise Exception("The user does not exist")
        hash = self.generate_hash(existing_user['salt'], password)
        if hash != existing_user['hash']: 
            raise Exception("Wrong Login")
        payload = {
            "email": existing_user['email'],
            "iat": get_int_from_datetime(datetime.now(timezone.utc)),
            "exp": get_int_from_datetime(datetime.now(timezone.utc) + timedelta(days=7)), 
        }
        return sign_message(payload)
        

    def authorize(self, authorization):
        try: 
            return verify_message(authorization)
        except:
            raise Exception("Authorization failed") 

