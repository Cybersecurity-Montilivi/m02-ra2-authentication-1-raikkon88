from flask import Flask, g
from flask import request
from flask import jsonify
from lib.users import Users
from lib.db import Db
from lib.crypto_utils import (generate_pem_file, SIGNING_KEY_FILE)
from log4python.Log4python import log
from os.path import exists

app = Flask(__name__)

if not exists(SIGNING_KEY_FILE):
    generate_pem_file()

@app.before_request
def open_database():
    g.db = Db()
    g.users = Users(g.db)

@app.route('/register', methods=['POST'])
def register(): 
    body = request.get_json()
    result = g.users.register(body['email'])
    return jsonify(result)


@app.route('/init', methods=['POST'])
def init(): 
    body = request.get_json()
    print(body)
    g.users.init(body["token"], body["password"])
    return jsonify('ok')

@app.route('/login', methods=['POST'])
def login(): 
    body = request.get_json()
    token = g.users.login(body["email"], body["password"])
    return jsonify(token)

@app.route('/verify', methods=['POST'])
def verify(): 
    body = request.get_json()
    payload = g.users.authorize(body['authorization'])
    return jsonify(payload)

@app.after_request
def close_database(response):
    g.db.close()
    return response

if __name__ == "__main__":
    app.run()