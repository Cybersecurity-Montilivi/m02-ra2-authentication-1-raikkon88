import secrets
from hashlib import pbkdf2_hmac

REGISTER_TOKEN_LENGTH = 64
ITERATIONS = 500000

class Users:

    def __init__(self, db):
        self.db = db

    def generate_hash(self, salt, password, email):
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
        existing_user['hash'] = self.generate_hash(
            existing_user["salt"], password, existing_user["email"])
        existing_user['token'] = None
