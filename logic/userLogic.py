import hashlib
import time

from logic import send_email
import os
import re
from dotenv import load_dotenv
from os import getenv

load_dotenv()

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
    if verify_password(user.password):
        user.password = hash_password(user.salt, user.password)
        sql.insertUser(user)
        return jsonify({'data':{'email': user.email}}), 200
    else:
        return error("Invalid password", 403)

def login(user):
    if getenv("SYS_SECURETY_LVL") == "SAFE":
        tries = sql.get_login_tries(user.email)[1]
        print(tries)
        if tries < 3:
            sql.update_login_tries(user.email, tries + 1)
        else:
            return error("Unauthorized - blocked", 401)

        data = sql.getUserByEmail(user)
        if not data:
            return error("Unauthorized", 401)
        user_db = User(data[0],data[1], bytes.fromhex(data[2]))
        if hash_password(user_db.salt, user.password) == user_db.password:
            sql.update_login_tries(user.email, 0)
            return user_to_json(data)
        else:
            return error("Unauthorized", 401)
    else:
        data = sql.getUserByEmail(user)
        if not data:
            return error("Unauthorized", 401)
        user_db = User(data[0], data[1], bytes.fromhex(data[2]))
        if hash_password(user_db.salt, user.password) == user_db.password:
            sql.update_login_tries(user.email, 0)
            return user_to_json(data)
        else:
            return error("Unauthorized", 401)


def forget_password(user):
    data = sql.getUserByEmail(user)
    if data is None:
        return error("Unauthorized", 401)
    # TODO: gen random pass and use SHA-1
    new_pass = "1234567890"
    send_email.send_new_password_email(user.email, new_pass)
    user.salt = os.urandom(32)
    user.password = hash_password(user.salt, new_pass)
    sql.update_user(user)
    return ok()


def change_password(user, new_password):
    data = sql.getUserByEmail(user)
    if not data:
        return error("Unauthorized", 401)
    user_db = User(data[0], data[1], bytes.fromhex(data[2]))
    old_password = user.password
    if hash_password(user_db.salt, user.password) == user_db.password:
        user.salt = os.urandom(32)
        if verify_password(new_password) and password_history_check(user.email, new_password):
            user.password = hash_password(user.salt, new_password)
            sql.update_user(user)
            sql.insert_history(user.email, old_password)
            return ok()
        else:
            return error("Invalid password",403)
    else:
        return error("Unauthorized", 401)


def hash_password(salt, password):
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return key.hex().__str__()


def password_history_check(email, password):
    if HISTORY_CHECK:
        return sql.valid_password_history(email, password)
    return True



def verify_password(password):
    # return false if password not valid
   # if len(password) < PASSWORD_MIN_LEN:
   #     return False
    if IS_SMALL_LETTERS and not any(char.islower() for char in password):
        return False
    if IS_BIG_LETTERS and not any(char.isupper() for char in password):
        return False
    if IS_NUMBERS and not bool(re.search(r'\d', password)):
        return False
    spacial_chars = ['@', '_', '!', '#', '$', '%', '^', '&', '*', '(', ')', '?', '/', '|', '}', '{', '~', ':']
    if SPECIAL_CHAR and not any((char in spacial_chars) for char in password):  # special character
        return False
    if DICT_CHECK and password_dict_check(password):
        return False
    return check_sqli(password)  # returns true if ' " < > = not exist else false


def password_dict_check(password):
    return False

    base_path = Path(__file__).parent
    file_path = (base_path / "./names.txt").resolve()

    with open(file_path, 'r') as f:
        for line in f.readline().strip():
            if line == password:
                return True
    return False

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



