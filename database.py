import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            try:
                self.connection = sqlite3.connect('database/users.db')
            except sqlite3.Error as error:
                print("Failed to insert Python variable into sqlite table", error)
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def add_user(self, prenom, nom, email, password):
        connect = self.get_connection()
        cur = connect.cursor()
        sql = """INSERT INTO 'regularsUsers'
                          ('first_name', 'last_name','email', 'password') 
                          VALUES (?, ?, ?, ?);"""
        data = (prenom, nom, email, password)
        cur.execute(sql, data)
        connect.commit()
        self.disconnect()

    def get_user(self, email):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT user_id,email,password FROM regularsUsers WHERE email= ?", (email,))
        result = cur.fetchone()
        self.disconnect()
        if result is None:
            return None
        else:
            return result

    def get_user_role(self, id):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT role_id FROM Users_Role WHERE user_id= ?", (id,))
        result = cur.fetchone()
        self.disconnect()
        if result is None:
            return None
        else:
            return result
