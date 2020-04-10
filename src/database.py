import sqlite3
from pprint import PrettyPrinter

class DbInterface:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread = False)
        self.cursor = self.conn.cursor()

    def add_visitor(self, chat_id):
        sql = 'INSERT INTO Visitors (chat_id) VALUES (?)'
        args = [chat_id]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("User exists")
            return False

    def authorize_payed_user(self, payment_id, chat_id, status, create_date, end_date):
        """ Inserts user to the table of paid users
        
        To make insertion more reliable
        you should provide arguments by name
        .authorizeUser(payment_id = 1, chat_id = 1,day = 1, time = 1, username = "lol", email = "kek")
        
        return if insertion was succesfull(True) or not (False)"""

        sql = 'INSERT INTO Payments (payment_id, chat_id, status, create_date, end_date) VALUES (?,?,?,?,?)'
        args = [payment_id, chat_id, status, create_date, end_date]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("User exists")
            return False

    def check_payed_user(self, chat_id):
        """ Checks out if provided user in our payments tables
        return boolean answer"""
        sql = 'SELECT EXISTS(SELECT * from Payments WHERE Chat_id = ?)'
        args = [chat_id]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
            return True if self.cursor.fetchall()[0][0] == 1 else False
        except sqlite3.IntegrityError:
            print("ERROR while checking the user")
            return False


    """GAMES SECTION"""

    def set_game(self, Name, Description, Location, Age, Type, Props):
        """ Inserts game to the database """
        sql = 'INSERT INTO Games (Name, Description, Location, Age, Type, Props) VALUES (?,?,?,?,?,?)'
        args = [Name, Description, Location, Age, Type, Props]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
            print(f"Game {Name} inserted succsesfully")
        except sqlite3.IntegrityError:
            print(f"ERROR while inserting {Name}")
            self.conn.commit()
    
    def get_games(self, Location = None, Age = None, Type = None, Props = None):
        sql = "SELECT Name, Description FROM Games WHERE "
        sql += f'Location LIKE \'%{Location}%\''
        if Age is not None:
            sql += f'AND (Age LIKE \'%{Age}%\') '
        if Type is not None:
            sql += f'AND (Type LIKE \'%{Type}%\')'
        if Props is not None:
            sql += f'AND (Props LIKE \'%{Props}%\')'
        try:
            self.cursor.execute(sql)#, args)
            data = self.cursor.fetchall()
            self.conn.commit()
            return data
        except:
            self.conn.commit()
            print(f"Your request {Location, Age, Type, Props} failed")

# DB = DbInterface('database.db')
# DB.add_visitor(2)
# print(DB.check_payed_user(2))