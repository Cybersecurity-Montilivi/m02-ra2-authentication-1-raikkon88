import secrets

REGISTER_TOKEN_LENGTH = 64

class Users:
    
    def __init__(self, db):
        self.db = db
        
    def register(self, email):
        existing_user = self.db.get_user_by_email(email)
        if existing_user != None:
            raise Exception("The user already exists")
        user = { "email": email, "token": secrets.token_urlsafe(REGISTER_TOKEN_LENGTH)}
        self.db.set_user(user)
        return user