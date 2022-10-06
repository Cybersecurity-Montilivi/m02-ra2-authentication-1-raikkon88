import secrets
import hashlib

REGISTER_TOKEN_LENGTH = 64


class Users:

    def __init__(self, db):
        self.db = db

    # TODO : Use hashlip.scrypt instead!!
    def generate_hash(self, salt, password, email):
        generator = hashlib.sha3_512()
        generator.update(salt)
        generator.update(password)
        generator.udpate(email)
        return generator.hexdigest()

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
