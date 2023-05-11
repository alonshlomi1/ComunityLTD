import mysql.connector
from logic.client import Client
from con_data import *



class sql():
    rows = None

    def __init__(self):
        self.con = mysql.connector.connect(host=HOST,
                                           user=USER,
                                           password=PASSWORD,
                                           database=DATABASE,
                                           port=PORT,
                                           auth_plugin=AUTH_PLUGIN)
        self.cur = self.con.cursor()

    def insertUser(self, user):
        self.rows = self.cur.execute("insert into users (user_email, user_password, user_salt) values(%s, %s, %s)", (user.email, user.password, user.salt.hex()))
        self.con.commit()


    def isValidUser(self, user):
        mySql_select_query = "select * from users where " + "user_email ='" + user.email + "';"
        self.cur.execute(mySql_select_query)
        rows = self.cur.fetchall()
        for r in rows:
            return True
        return False


    def getUserByEmail(self, user):
        mySql_select_query = "select * from users where " + "user_email ='" + user.email + "';"
        self.cur.execute(mySql_select_query)
        data = self.cur.fetchone()
        if data:
            return data
        return False


    def update_user(self, user):
        self.rows = self.cur.execute("update users set user_password = %s ,user_salt = %s  where user_email = %s;",(user.password, user.salt.hex(), user.email))
        self.con.commit()

    def getAllClients(self):
        allClients = []
        mySql_select_query = "select * from clients"
        self.cur.execute(mySql_select_query)
        rows = self.cur.fetchall()
        for r in rows:
            allClients.append(
                Client(r[1], r[2], r[3], r[4], r[0])
            )
        return allClients

    def insertclient(self, client):
        mySql_insert_query = "insert into clients" \
                             "(client_id, client_first_name, client_last_name, client_phone, client_email)" \
                             "values('" + client.id + "', '" + client.first_name + "', '" + client.last_name +\
                             "', '" + client.phone + "', '" + client.email + "');"
        self.rows = self.cur.execute(mySql_insert_query)
        self.con.commit()
