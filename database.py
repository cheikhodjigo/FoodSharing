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
        sql = """INSERT into regularsUsers
                          ('first_name', 'last_name','email', 'password') 
                          VALUES (?, ?, ?, ?);"""
        data = (prenom, nom, email, password)
        cur.execute(sql, data)
        connect.commit()
        sql = """INSERT into Users_Role
                                 ('user_id', 'role_id') 
                                 VALUES ((SELECT user_id from regularsUsers WHERE email=?), 2);"""
        data = (email,)
        cur.execute(sql, data)
        connect.commit()

    def change_user_information(self, prenom, nom, email, phonenumber, id):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("UPDATE regularsUsers SET first_name=?, last_name=?, email=?, phonenumber=? WHERE user_id= ?",
                    (prenom, nom, email, phonenumber, id,))
        connect.commit()

    def change_user_status(self, id, status):
        connect = self.get_connection()
        cur = connect.cursor()
        if status == "Actif":
            cur.execute("UPDATE regularsUsers SET status='Inactif' WHERE user_id= ?",
                        (id,))
        else:
            cur.execute("UPDATE regularsUsers SET status='Actif' WHERE user_id= ?",
                        (id,))
        connect.commit()

    def get_user_by_mail(self, email):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT user_id,email,password,status FROM regularsUsers WHERE email= ?", (email,))
        result = cur.fetchone()
        if result is None:
            return None
        else:
            return result

    def get_user_by_id(self, id):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT * FROM regularsUsers WHERE user_id= ?", (id,))
        result = cur.fetchone()
        if result is None:
            return None
        else:
            return result

    def get_user_offers(self, userd_id):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT * FROM Offers WHERE offer_user_id = ?", (userd_id,))
        result = cur.fetchall()
        if result is None:
            return None
        else:
            return result

    def search_offers(self, key_word, categorie):
        connect = self.get_connection()
        cur = connect.cursor()
        if categorie == "-1" and key_word:
            cur.execute("SELECT * FROM Offers WHERE offer_title LIKE ?", ('%'+key_word+'%',))
        elif key_word and categorie != "-1":
            cur.execute("SELECT * FROM Offers WHERE offer_title LIKE ? AND offer_categorie_id= ?", ('%'+key_word+'%', categorie,))
        elif not key_word and categorie != "-1":
            cur.execute("SELECT * FROM Offers WHERE offer_categorie_id = ? ",
                        (categorie,))
        else:
            cur.execute("SELECT * FROM Offers")
        result = cur.fetchall()
        if result is None:
            return None
        else:
            return result

    def get_all_offers(self):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT * FROM Offers")
        result = cur.fetchall()
        if result is None:
            return None
        else:
            return result

    def get_categories(self):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT categorie_id, categorie_title FROM Categories ORDER BY categorie_title ASC")
        result = cur.fetchall()
        if result is None:
            return None
        else:
            return result

    def get_offers(self, user_id):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT * FROM Offers WHERE offer_user_id = ?", (user_id,))
        result = cur.fetchall()
        if result is None:
            return None
        else:
            return result

    def get_offer_by_id(self, offer_id):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT * FROM Offers WHERE offer_id = ?", (offer_id,))
        result = cur.fetchone()
        if result is None:
            return None
        else:
            return result

    def delete_offer_from_user(self, offer_id):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("delete from Offers where offer_id = ?", (offer_id,))
        connect.commit()

    def add_offer(self, categorie, user_id, title, description, price):
        connect = self.get_connection()
        cur = connect.cursor()
        sql = """INSERT INTO 'Offers'
                          ('offer_categorie_id', 'offer_user_id', 'offer_title','offer_description', 'offer_price') 
                          VALUES (?, ?, ?, ?, ?);"""
        data = (categorie, user_id, title, description, price)
        cur.execute(sql, data)
        connect.commit()

    def get_user_role(self, user_id):
        connect = self.get_connection()
        cur = connect.cursor()
        sql = """SELECT title FROM regularsUsers 
                    INNER JOIN Users_Role ON regularsUsers.user_id = Users_Role.user_id 
                    INNER JOIN Roles On Roles.role_id = Users_Role.role_id WHERE regularsUsers.user_id=?"""
        data = (user_id,)
        cur.execute(sql, data)
        result = cur.fetchone()
        if result is None:
            return None
        else:
            return result

    def get_all_users(self):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT * FROM regularsUsers")
        result = cur.fetchall()
        if result is None:
            return None
        else:
            return result

    def get_all_users_except_actual(self, id):
        connect = self.get_connection()
        cur = connect.cursor()
        cur.execute("SELECT * FROM regularsUsers WHERE user_id != ?", (id,))
        result = cur.fetchall()
        if result is None:
            return None
        else:
            return result
