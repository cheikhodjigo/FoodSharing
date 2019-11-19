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


    def addUser(self,id_user, prenom, nom, email, password):
        connect = self.get_connection()
        cur = connect.cursor()
        sql = """INSERT INTO 'regularsUsers'
                          ('user_id', 'first_name', 'last_name','email', 'password') 
                          VALUES (?, ?, ?, ?, ?);"""

        data = (id_user, prenom, nom,email, password)
        cur.execute(sql,data)
        connect.commit()