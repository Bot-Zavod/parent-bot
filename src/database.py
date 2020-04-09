import sqlite3
from pprint import PrettyPrinter

class DbInterface:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread = False)
        self.cursor = self.conn.cursor()

    # def getGames(self, type=None, age=None, amount=None, location=None, props=None):
    #     sql = "SELECT DISTINCT Id FROM Games WHERE "
    #     args = [type]
    #     sql += 'Type=?'
    #     if age is not None:
    #         sql += 'AND (Age=? OR Age is NULL)'
    #         args.append(age)
    #     if amount is not None:
    #         sql += 'AND (Amount=? OR Amount is NULL)'
    #         args.append(amount)
    #     if location is not None:
    #         sql += 'AND (Location=? OR Location is NULL)'
    #         args.append(location)
    #     if props is not None:
    #         sql += 'AND (Props=? OR Props is NULL)'
    #         args.append(props)
    #     self.cursor.execute(sql, args)
    #     data = self.cursor.fetchall()
    #     return data if len(data) == 0 else tuple(d[0] for d in data)

    def authorizeUser(self, payment_id, chat_id, day, time, username, email):
        """ Inserts user to the table of paid users
        
        To make insertion more reliable
        you should provide arguments by name
        .authorizeUser(payment_id = 1, chat_id = 1,day = 1, time = 1, username = "lol", email = "kek")
        
        return if insertion was succesfull(True) or not (False)"""
        sql = 'INSERT INTO Payments (payment_id, chat_id, day, time, username, email) VALUES (?,?,?,?,?,?)'
        args = [payment_id, chat_id, day, time, username, email]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("User exists")
            return False

    def checkUser(self, chat_id):
        """ Checks out if provided user in our payments tables
        return boolean answer"""
        sql = 'SELECT EXISTS(SELECT * from Payments Where Chat_id = ?)'
        args = [chat_id]
        self.cursor.execute(sql, args)
        return True if self.cursor.fetchall()[0][0] == 1 else False


    """GAMES SECTION

    CREATE TABLE "Games" (
        "Name"	TEXT,
        "Description"	TEXT,
        "Location"	TEXT,
        "Age"	TEXT,
        "Type"	TEXT,
        "Props"	TEXT
    );"""

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

DB = DbInterface('database.db')
# games = DB.get_games("дома", "обучающая", "3-4", "да")
# PrettyPrinter().pprint(games)