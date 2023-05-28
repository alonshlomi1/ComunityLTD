import hashlib
from flask_mail import Mail, Message
import os
import re

import psycopg2

from logic.user import User
from flask import Response, jsonify
from con_data import *
from database.sqlConnection import sql

sql = sql()

def user_to_json(user):
    json_body = {
        'data': {
            'email': user[0]
        }
    }
    return jsonify(json_body), 200

def add_user(user):
    data = sql.getUserByEmail(user)
    if data:
        return error("Email taken", 409)
    user.salt = os.urandom(32)
    user.password = hash_password(user.salt, user.password)
    sql.insertUser(user)
    return jsonify({'data':{'email': user.email}}), 200


def login(user):
    data = sql.getUserByEmail(user)
    if not data:
        return error("Unauthorized", 401)
    user_db = User(data[0],data[1], bytes.fromhex(data[2]))
    if hash_password(user_db.salt, user.password) == user_db.password:
        return user_to_json(data)
    else:
        return error("Unauthorized", 401)
        #not found?

def forget_password(user):
    data = sql.getUserByEmail(user)
    if data is None:
        return error("Unauthorized", 401)
    new_pass = "1234567890"
    # TODO: send email with new password
    user.salt = os.urandom(32)
    user.password = hash_password(user.salt, new_pass)
    sql.update_user(user)
    return ok()


def change_password(user, new_password):
    data = sql.getUserByEmail(user)
    print(user.email)
    if not data:
        return error("Unauthorized", 401)
    user_db = User(data[0], data[1], bytes.fromhex(data[2]))
    if hash_password(user_db.salt, user.password) == user_db.password:
        user.salt = os.urandom(32)
        user.password = hash_password(user.salt, new_password)
        sql.update_user(user)
        return ok()
    else:
        return error("Unauthorized", 401)


def hash_password(salt, password):
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return key.hex().__str__()


def verify_password(password):
    # return false if password not valid
    if len(password) < PASSWORD_MIN_LEN:
        return 1
    if IS_SMALL_LETTERS and not any(char.islower() for char in password):
        return 2
    if IS_BIG_LETTERS and not any(char.isupper() for char in password):
        return 3
    if IS_NUMBERS and not bool(re.search(r'\d', password)):
        return 4
    spacial_chars = ['@', '_', '!', '#', '$', '%', '^', '&', '*', '(', ')', '?', '/', '|', '}', '{', '~', ':']
    if SPECIAL_CHAR and not any((char in spacial_chars) for char in password):  # special character
        return 5

    if password_dict_check(password):
        return False
    return check_sqli(password)  # returns true if ' " < > = not exist else false


def password_dict_check(password):
    return True
    """ 
    base_path = Path(__file__).parent
    file_path = (base_path / "./realhuman_phill.txt").resolve()

    with open(file_path, 'r') as f:
        for line in f.readline().strip():
            if line == password:
                return True
    return False
    """
def check_sqli(data):
    return True
    """
    string_check = re.compile('''[><'"=]''')
    if string_check.search(str(data)) is not None or not data:  # for sqli
        return False
    return True
    """
def ok():
    return jsonify({}), 200


def invalid_details():
    return jsonify({}), 400


def not_found():
    return jsonify({}), 404


def error(msg, flag):
    return jsonify({"error": msg}), flag



