import json
import argparse
from lib.users import Users
from lib.db import Db
from lib.crypto_utils import (generate_pem_file, SIGNING_KEY_FILE)
from log4python.Log4python import log
from os.path import exists


parser = argparse.ArgumentParser(
    description='Auth and names generator params', prog="generator")
parser.add_argument('-r', '--register',
                    help='Register a new user, requested parameters: { email }', type=str, default=None)
parser.add_argument(
    '-l', '--login', help='Login action will print a bearer token, requested parameters: { username, password }', type=str, default=None)
parser.add_argument(
    '-i', '--init', help='Init action, will print success or failed, requested parameters: { token, password }', type=str, default=None)
parser.add_argument(
    '-a', '--authorize', help='Authorization action, requested parameters: { authorization }', type=str, default=None)
args = vars(parser.parse_args())

Logger = log("Generator")

db = Db()
if not exists(SIGNING_KEY_FILE):
    generate_pem_file()


def register(body):
    users = Users(db)
    user = users.register(body["email"])
    return user["token"]

def init(body):
    users = Users(db)
    users.init(body["token"], body["password"])

def login(body): 
    users = Users(db)
    return users.login(body["email"], body["password"])

def authorize(body):
    users = Users(db)
    return users.authorize(body['authorization'])


try:
    if args['register'] != None:
        body = json.loads(args['register'])
        token = register(body)
        Logger.info(f'{token}')

    elif args['init'] != None:
        body = json.loads(args['init'])
        init(body)

    elif args['login'] != None:
        body = json.loads(args['login'])
        bearer_token = login(body)
        Logger.info(f'{bearer_token}')

    elif args['authorize'] != None: 
        body = json.loads(args['authorize'])
        payload = authorize(body)
        Logger.info(f'{payload}')

    else: 
        Logger.error('Should not process any request')

except Exception as e:
    Logger.error(str(e))

db.close()
