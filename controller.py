from flask import Flask, request
from flask_cors import CORS
from logic.user import User
from logic.client import Client
from logic.userLogic import *
from logic.clientLogic import *


from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
"""
if __name__ == "__main__":
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.run(debug=True)
"""

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






