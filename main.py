import json
import argparse
from lib.users import Users
from lib.db import Db
from log4python.Log4python import log

parser = argparse.ArgumentParser(
    description='Auth and names generator params', prog="generator")
parser.add_argument('-r', '--register',
                    help='Register a new user, requested parameters: { email }', type=str, default=None)
parser.add_argument(
    '-l', '--login', help='Login action will print a bearer token, requested parameters: { username, password }', type=str, default='./generated.json')
parser.add_argument(
    '-i', '--init', help='Init action, will print success or failed, requested parameters: { token, password }', type=str, default=10)
# parser.add_argument('-b', '--body', help='Body requested from the action', type=str, default=None)
args = vars(parser.parse_args())

Logger = log("Generator")

db = Db()


def register(body):
    users = Users(db)
    user = users.register(body["email"])
    return user["token"]


def init(body):
    users = Users(db)
    users.init(body["token"], body["password"])


try:
    if args['register'] != None:
        body = json.loads(args['register'])
        token = register(body)
        Logger.info(f'{token}')

    elif args['init'] != None:
        body = json.loads(args['init'])
        init(body)

    elif args['login'] != None:
        Logger.info('login')


except Exception as e:
    Logger.error(str(e))

db.close()
