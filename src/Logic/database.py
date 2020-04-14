import sqlite3
import os


class DbInterface:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread = False)
        self.cursor = self.conn.cursor()



    """
    
    USER SECTION
    
    """
    def add_user(self, chat_id, username=None, first_name=None, last_name=None, email=None, phone=None):
        sql = 'INSERT INTO Users (chat_id, username, first_name, last_name, email, phone) VALUES (?,?,?,?,?,?)'
        args = [chat_id, username, first_name, last_name, email, phone]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("User exists")
            return False
    
    def check_user(self, chat_id):
        sql = 'SELECT EXISTS(SELECT * from Users WHERE chat_id = ?)'
        args = [chat_id]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
            return True if self.cursor.fetchall()[0][0] == 1 else False
        except sqlite3.IntegrityError:
            print("ERROR while checking the user")
            return False

    """

    PAYMENT SECTION
    
    """
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
        sql = 'SELECT EXISTS(SELECT * from Payments WHERE chat_id = ?)'
        args = [chat_id]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
            return True if self.cursor.fetchall()[0][0] == 1 else False
        except sqlite3.IntegrityError:
            print("ERROR while checking the user")
            return False


    """
    
    GAMES SECTION
    
    """
    def set_game(self, Name, Description, Location, Age, Type, Props):
        """ Inserts game to the database """
        sql = 'INSERT INTO Games (Name, Description, Location, Age, Type, Props) VALUES (?,?,?,?,?,?)'
        args = [Name, Description, Location, Age, Type, Props]
        try:
            self.cursor.execute(sql, args)
            print(f"Game {Name} inserted succsesfully")
        except sqlite3.IntegrityError:
            print(f"ERROR while inserting {Name}")
        finally:
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
        data = False
        try:
            self.cursor.execute(sql)#, args)
            data = self.cursor.fetchall()
        except:
            print(f"Your request {Location, Age, Type, Props} failed")
        finally:
            self.conn.commit()
        return data

    def get_game(self, game):
        sql = "SELECT Description FROM Games WHERE Name = (?)"
        args = [game]
        data = False
        try:
            self.cursor.execute(sql, args)
            data = self.cursor.fetchall()[0][0]
        except:
            print(f"Your game {game} does not exist or some other shit happened")
        finally:
            self.conn.commit()
        return data

db_path = os.getcwd() + "/database.db"
DB = DbInterface(db_path)

if __name__ == "__main__":
    # file = "database.db"
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # db_path = os.path.join(BASE_DIR, file)
    db_path = os.getcwd() + "/database.db"
    DB = DbInterface(db_path)
    DB.add_user(383327735, 'alexeymarkovski', 'Alexey', 'Markovski', '380952793306')
    print(DB.check_payed_user(383327735))