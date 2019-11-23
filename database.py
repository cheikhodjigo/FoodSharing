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

    def get_user_by_mail(self, email):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT user_id,email,password FROM regularsUsers WHERE email= ?", (email,))
        result = cur.fetchone()
        self.disconnect()
        if result is None:
            return None
        else:
            return result

    def get_user_by_id(self, id):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT * FROM regularsUsers WHERE user_id= ?", (id,))
        result = cur.fetchone()
        self.disconnect()
        if result is None:
            return None
        else:
            return result

    def get_user_offers(self, userd_id):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT * FROM Offers WHERE offer_user_id = ?", (userd_id,))
        result = cur.fetchall()
        self.disconnect()
        if result is None:
            return None
        else:
            return result

    def get_all_offers(self):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT * FROM Offers")
        result = cur.fetchall()
        self.disconnect()
        if result is None:
            return None
        else:
            return result

    def get_categories(self):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT categorie_id,categorie_title FROM Categories ORDER BY categorie_title ASC")
        result = cur.fetchall()
        self.disconnect()
        if result is None:
            return None
        else:
            return result

    def get_offers(self, user_id):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT * FROM Offers WHERE offer_user_id = ?", (user_id,))
        result = cur.fetchall()
        self.disconnect()
        if result is None:
            return None
        else:
            return result

    def get_offer_by_id(self, offer_id):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT * FROM Offers WHERE offer_id = ?", (offer_id,))
        result = cur.fetchone()
        self.disconnect()
        if result is None:
            return None
        else:
            return result

    def delete_offer_from_user(self, offer_id):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("delete from Offers where offer_id = ?", (offer_id,))
        connect.commit()
        self.disconnect()

    def add_offer(self, categorie, user_id, title, description, price):
        connect = self.get_connection()
        cur = connect.cursor()
        sql = """INSERT INTO 'Offers'
                          ('offer_categorie_id', 'offer_user_id', 'offer_title','offer_description', 'offer_price') 
                          VALUES (?, ?, ?, ?, ?);"""
        data = (categorie, user_id, title, description, price)
        cur.execute(sql, data)
        connect.commit()
        self.disconnect()

    def get_user_role(self, id):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT title FROM Roles WHERE user_id EXISTS (SELECT user_id FROM Users_Role WHERE user_id = ?)", (id,))
        result = cur.fetchone()
        self.disconnect()
        if result is None:
            return None
        else:
            return result
