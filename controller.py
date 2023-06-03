import ssl
import sys

from flask import Flask, request
from flask_sslify import SSLify

from logic.client import Client
from logic.userLogic import *
from logic.clientLogic import *
from flask_cors import CORS
from OpenSSL import SSL
import bleach
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
sslify = SSLify(app, subdomains=True)
CORS(app)


@app.route('/login', methods=['POST'])
def get_current_user():
    data = request.get_json()
    return login(User(data['email'], bleach.clean(data['password'])))


@app.route('/submitNewUser', methods=['POST'])
def add_new_user():
    data = request.get_json()
    return add_user(User(bleach.clean(data['email']), bleach.clean(data['password'])))


@app.route('/forgetPassword', methods=['POST'])
def gen_new_password():
    data = request.get_json()
    return forget_password(User(bleach.clean(data['email'])))


@app.route('/changePassword', methods=['POST'])
def update_user_password():
    data = request.get_json()
    return change_password(User(bleach.clean(data['email']), bleach.clean(data['old_password'])),
                           bleach.clean(data['new_password']))


@app.route('/getAllClients', methods=['POST'])
def get_all_clients():
    return all_clients()


@app.route('/insertNewClient', methods=['POST'])
def add_new_client():
    data = request.get_json()
    #    comment = bleach.clean(request.form.get('comment'))
    if getenv("SYS_SECURETY_LVL") == "UNSAFE":
        return add_client(Client(data['first_name'], bleach.clean(data['last_name']), data['phone'], data['email']))
    else:
        return add_client(
            Client(bleach.clean(data['first_name']), bleach.clean(data['last_name']), bleach.clean(data['phone']),
                   bleach.clean(data['email'])))


if __name__ == '__main__':

    #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.maximum_version = ssl.TLSVersion.TLSv1_3
    context.load_cert_chain("cert.pem", "key.pem")
    app.run(host='127.0.0.1', port=5000, debug=True, ssl_context=context)




    """
    Open a new tab in Google Chrome and enter chrome://flags in the address bar.
    Search for the flag called "Allow invalid certificates for resources loaded from localhost."
    Enable this flag by clicking on the "Enable" button.
    Relaunch Google Chrome to apply the changes.
    """
