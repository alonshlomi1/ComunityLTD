from flask import Flask, request
from flask_sslify import SSLify

from flask_cors import CORS
from logic.user import User
from logic.client import Client
from logic.userLogic import *
from logic.clientLogic import *
from flask import Flask
from flask_cors import CORS
from OpenSSL import SSL

import ssl

app = Flask(__name__)
sslify = SSLify(app, subdomains=True)
CORS(app)


@app.route('/login', methods=['POST'])
def get_current_user():
    data = request.get_json()
    return login(User(data['email'], data['password']))


@app.route('/submitNewUser', methods=['POST'])
def add_new_user():
    data = request.get_json()
    return add_user(User(data['email'], data['password']))


@app.route('/forgetPassword', methods=['POST'])
def gen_new_password():
    data = request.get_json()
    return forget_password(User(data['email']))


@app.route('/changePassword', methods=['POST'])
def update_user_password():
    data = request.get_json()
    return change_password(User(data['email'], data['old_password']), data['new_password'])


@app.route('/getAllClients', methods=['POST'])
def get_all_clients():
    return all_clients()


@app.route('/insertNewClient', methods=['POST'])
def add_new_client():
    data = request.get_json()
    return add_client(Client(data['first_name'],data['last_name'],data['phone'],data['email']))






if __name__ == '__main__':
    context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
    context.use_privatekey_file('./private.key')
    context.use_certificate_file('./certificate.crt')
    app.run(host='127.0.0.1', debug=True,  port=500, ssl_context=context)

    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('./certificate.crt', './private.key')
    app.run(host='127.0.0.1', port=5000, ssl_context=context)
    """