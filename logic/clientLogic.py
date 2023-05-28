import json

from flask import Response, jsonify
from database.sqlConnection import sql

sql = sql()


def add_client(client):
    sql.insertClient(client)
    return jsonify({}),200

def all_clients():
    res = sql.getAllClients()
    response_body = json.dumps([obj.__dict__ for obj in res])
    return response_body, 200