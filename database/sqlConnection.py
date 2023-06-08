import mysql.connector
from logic.client import Client
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class sql():
    rows = None

    def connect(self):
        return mysql.connector.connect(host=getenv("HOST"),
                                       user=getenv("USER"),
                                       password=getenv("PASSWORD"),
                                       database=getenv("DATABASE"),
                                       port=getenv("PORT"),
                                       auth_plugin=getenv("AUTH_PLUGIN"))

    def insertUser(self, user):
        con = self.connect()
        cur = con.cursor()

        if getenv("SYS_SECURITY_LVL") == "SAFE" or getenv("SYS_SECURITY_LVL") == "XSS":
            self.rows = cur.execute("insert into users (user_email, user_password, user_salt) values(%s, %s, %s)",
                                    (user.email, user.password, user.salt.hex()))
            con.commit()
        else:
            mySql_query = "insert into users (user_salt, user_password, user_email) " \
                          "values('" + user.salt.hex() + "', '" + user.password + "', '" + user.email + "');"
            try:
                cur.execute(mySql_query, multi=True)
            except Exception as e:
                print(e)
                cur.close()
                con.close()
                return False
        cur.close()
        con.close()
        self.insert_tries(user)
        return True

    def insert_tries(self, user):
        con = self.connect()
        cur = con.cursor()
        try:
            cur.execute("insert into login_tries (user_email, tries) values(%s, %s)",
                                (user.email, 0,))
            con.commit()
        except Exception as e:
            print(e)
            cur.close()
            con.close()
        cur.close()
        con.close()

    def insert_history(self, email, password):
        con = self.connect()
        cur = con.cursor()
        self.rows = cur.execute("insert into users_history (user_email, user_password) values(%s, %s)",
                                (email, password,))
        con.commit()
        cur.close()
        con.close()

    def get_login_tries(self, email):
        con = self.connect()
        cur = con.cursor()

        self.rows = cur.execute("select * from login_tries where user_email = %s ;", (email,))
        data = cur.fetchone()
        cur.close()
        if data:
            return data
        return False

    def update_login_tries(self, email, tries):
        con = self.connect()
        cur = con.cursor()

        self.rows = cur.execute("update login_tries set tries = %s where user_email = %s;",
                                (tries, email,))
        con.commit()
        cur.close()
        con.close()

    def isValidUser(self, user):
        con = self.connect()
        cur = con.cursor()

        self.rows = cur.execute("select * from users where user_email = %s ;", (user.email,))
        rows = cur.fetchall()
        cur.close()
        for r in rows:
            return True
        return False

    def valid_password_history(self, email, password):
        con = self.connect()
        cur = con.cursor()

        self.rows = cur.execute("select * from users_history where user_email = %s and user_password = %s;",
                                (email, password))
        rows = cur.fetchall()
        cur.close()
        con.close()
        for r in rows:
            return False
        return True

    def getUserByEmail(self, user):
        con = self.connect()
        cur = con.cursor()
        if getenv("SYS_SECURITY_LVL") == "SAFE" or getenv("SYS_SECURITY_LVL") == "XSS":
            self.rows = cur.execute("select * from users where user_email = %s ;", (user.email,))
        else:
            mySql_select_query = "select * from users where user_email ='" + user.email + "';"
            try:
                cur.execute(mySql_select_query, multi=True)
            except:
                return False
        data = cur.fetchall()
        cur.close()
        con.close()
        if data:
            return data[0]
        return False

    def update_user(self, user):
        con = self.connect()
        cur = con.cursor()

        self.rows = cur.execute("update users set user_password = %s ,user_salt = %s  where user_email = %s;",
                                (user.password, user.salt.hex(), user.email))
        con.commit()
        cur.close()
        con.close()

    def getAllClients(self):
        con = self.connect()
        cur = con.cursor()

        allClients = []
        mySql_select_query = "select * from clients"
        cur.execute(mySql_select_query)
        rows = cur.fetchall()
        cur.close()
        con.close()
        for r in rows:
            allClients.append(
                Client(r[1], r[2], r[3], r[4], r[0])
            )
        return allClients

    def insertClient(self, client):
        con = self.connect()
        cur = con.cursor()

        if getenv("SYS_SECURITY_LVL") == "SAFE" or getenv("SYS_SECURITY_LVL") == "XSS":
            self.rows = cur.execute("insert into clients (client_id, client_first_name, client_last_name, "
                                    "client_phone, client_email) values(%s, %s, %s, %s, %s)", (client.id,
                                                                                               client.first_name,
                                                                                               client.last_name,
                                                                                               client.phone,
                                                                                               client.email))
            con.commit()

        else:
            mySql_select_query = "insert into clients (client_id, client_first_name, client_last_name, " \
                                 "client_phone, client_email) values('" + client.id + "', '" \
                                 + client.first_name + "', '" \
                                 + client.last_name + "', '" \
                                 + client.phone + "', '" \
                                 + client.email + "');"
            cur.execute(mySql_select_query, multi=True)

        cur.close()
        con.close()
