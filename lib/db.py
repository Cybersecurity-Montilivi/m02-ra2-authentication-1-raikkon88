from genericpath import exists
import json
import pydash

DB_FILENAME = 'db.json'


class Db:

    def __init__(self):
        if exists(DB_FILENAME): 
            f = open(DB_FILENAME)
            db = json.load(f)
            f.close()
            self.db = db
        else: 
            self.db = { "users": [] }

    def close(self):
        with open(DB_FILENAME, 'w') as writer:
            json.dump(self.db, writer, indent=4)

    # GETTERS
    def get_users(self):
        return self.db["users"]

    def get_user(self, attr, value):
        return pydash.find(self.db["users"], lambda x: x[attr] == value)

    def get_user_by_token(self, token):
        return self.get_user("token", token)

    def get_user_by_email(self, email):
        return self.get_user("email", email)

    # SETTERS

    def set_user(self, user):
        self.db["users"].append(user)
