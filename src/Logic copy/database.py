import sqlite3
import os
from os import path, getcwd
import time
from pprint import pprint


class DbInterface:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        sql_tables = [
            # Games table
            """
            CREATE TABLE IF NOT EXISTS "Games" (
            "Name"	TEXT,
            "Description"	TEXT,
            "Location"	TEXT,
            "Age"	TEXT,
            "Type"	TEXT,
            "Props"	TEXT)
            """,

            # Payed_Users table
            """
            CREATE TABLE IF NOT EXISTS "Payments" (
            "payment_id"	INTEGER NOT NULL UNIQUE,
            "chat_id"	INTEGER,
            "status"	VARCHAR(50) DEFAULT NULL,
            "create_date"	DATETIME,
            "end_date"	DATETIME,
            "order_id"	varchar(50),
            PRIMARY KEY("payment_id"))
            """,

            # Users table
            """
            CREATE TABLE IF NOT EXISTS "Users" (
            "chat_id"	INTEGER UNIQUE)
            """
        ]

        for sql in sql_tables:
            self.cursor.execute(sql)
            self.conn.commit()

    # save id to Users
    def save_id(self, chat_id) -> None:
        sql = "INSERT OR IGNORE INTO Users (chat_id) values(?)"
        args = [chat_id]
        try:
            self.cursor.execute(sql, args)
        except:
            print(f"Saving {chat_id} failed")
        finally:
            self.conn.commit()

    # return number of [visitors, subscribed, unsubscribed]
    def users_count(self) -> list:
        sql = "SELECT COUNT(*) FROM Users"
        try:
            self.cursor.execute(sql)
            all_user = self.cursor.fetchall()[0][0]
        except:
            print(f"Check failed")
        finally:
            self.conn.commit()

        sql = "SELECT COUNT(*) FROM Payments WHERE status!='unsubscribed'"
        try:
            self.cursor.execute(sql)
            payed_user = self.cursor.fetchall()[0][0]
        except:
            print(f"Check failed")
        finally:
            self.conn.commit()

        sql = "SELECT COUNT(*) FROM Payments"
        try:
            self.cursor.execute(sql)
            all_payed_user = self.cursor.fetchall()[0][0]
        except:
            print(f"Check failed")
        finally:
            self.conn.commit()

        return [all_user, payed_user, all_payed_user-payed_user]

    # return chat_id list of passed user category
    def get_users(self, group=None) -> list:
        sql = "SELECT chat_id FROM Users"
        if group != None:
            if group == "PAYED":
                sql = "SELECT chat_id FROM Payments WHERE status!='unsubscribed'"
            elif group == "UNPAYED":
                sql = "SELECT chat_id FROM Payments WHERE status='unsubscribed'"
        try:
            self.cursor.execute(sql)
            answer = self.cursor.fetchall()
            if answer != []:
                users = answer[0]
            else:
                users = []
        except:
            print(f"Check failed")
        finally:
            self.conn.commit()
        return users

    """
    ===============
    PAYMENT SECTION
    ===============
    """

    def check_payed_user(self, chat_id):
        # Checks out if provided user in our payments tables return boolean answer
        sql = "SELECT EXISTS(SELECT * FROM Payments WHERE chat_id = (?) AND (?) <= end_date)"
        args = [chat_id, int(time.time())]
        answer = False
        # print(int(time.time()))
        try:
            self.cursor.execute(sql, args)
            cursor = self.cursor.fetchall()[0][0]
           # print('Cursor')
           # print(cursor)
            if cursor == 1:
                answer = True
            else:
                answer = False
        except sqlite3.IntegrityError:
            print("ERROR while checking the user")
        finally:
            self.conn.commit()
            return answer

    def is_subscribed(self, chat_id):
        """ Checks out if provided user in our payments tables
        return boolean answer"""
        sql = "SELECT EXISTS(SELECT * FROM Payments WHERE chat_id = (?) AND status = 'subscribed')"
        args = [chat_id]
        answer = False
        # print(int(time.time()))
        try:
            self.cursor.execute(sql, args)
            cursor = self.cursor.fetchall()[0][0]
           # print('Cursor')
           # print(cursor)
            if cursor == 1:
                answer = True
            else:
                answer = False
        except sqlite3.IntegrityError:
            print("ERROR while checking the user")
        finally:
            self.conn.commit()
            return answer

    def get_payment_id(self, chat_id):
        sql = "SELECT payment_id FROM Payments WHERE chat_id = (?)"
        args = [chat_id]
        data = None
        try:
            self.cursor.execute(sql, args)
            data = self.cursor.fetchall()[0][0]
        except:
            print(f"Your request get_payment_id {chat_id} failed")
        finally:
            self.conn.commit()
            return data

    def set_status(self, chat_id, status):
        sql = "UPDATE Payments SET status = (?) WHERE chat_id = (?)"
        args = [status, chat_id]
        data = None
        try:
            self.cursor.execute(sql, args)
            data = self.cursor.fetchall()[0][0]
        except:
            print(f"Updating status = {status} to {chat_id} failed")
        finally:
            self.conn.commit()
            return data

    def get_order_id(self, chat_id):
        sql = "SELECT order_id FROM Payments WHERE chat_id = (?)"
        args = [chat_id]
        data = None
        try:
            self.cursor.execute(sql, args)
            data = self.cursor.fetchall()[0][0]
        except:
            print(f"Your request get_order_id {chat_id} failed")
        finally:
            self.conn.commit()
            return data

    def unsubscribe_user(self, payment_id):
        sql = "UPDATE Payments SET status = ('unsubscribed') WHERE payment_id = (?)"
        args = [payment_id]
        data = False
        try:
            self.cursor.execute(sql, args)
            data = True
        except:
            print(f"Your request unsubscribe_user {payment_id} failed")
        finally:
            self.conn.commit()
            return data

    # return all payment database for admin spreadsheet
    def get_payments_data(self):
        sql = "SELECT * FROM Payments"
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(f"SELECT failed {e}")
        finally:
            self.conn.commit()
            return self.cursor.fetchall()

    """
    ================
    GAMES SECTION
    =================
    """
    # cleans games table before update

    def delete_games(self):
        sql = "DELETE FROM Games"
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(f" Delete shit happened {e}")
        finally:
            self.conn.commit()
        return "Delete done"

    # insert multiple games to the database at once
    def set_games(self, games_to_insert):
        sql = 'INSERT INTO Games (Name, Description, Location, Type, Age, Props) VALUES (?,?,?,?,?,?)'
        try:
            self.cursor.executemany(sql, games_to_insert)
        except Exception as e:
            print(f"ERROR while inserting {e}")
        finally:
            self.conn.commit()

    # return all games+name that sutisfy the qequirments
    def get_games(self, Location=None, Type=None,  Age=None, Props=None):
        sql = "SELECT Name, Description FROM Games WHERE "
        sql += f'(Location LIKE \'%{Location}%\' OR Location="")'
        if Age is not None:
            sql += f'AND (Age LIKE \'%{Age}%\' OR Age="")'
        if Type is not None:
            sql += f'AND (Type LIKE \'%{Type}%\' OR Type="")'
        if Props is not None:
            sql += f'AND (Props LIKE \'%{Props}%\' OR Props="")'
        data = []
        try:
            self.cursor.execute(sql)  # , args)
            data = self.cursor.fetchall()
        except:
            print(f"Your request {Location, Age, Type, Props} failed")
        finally:
            self.conn.commit()
        return data

    # return game with a passed name
    def get_game(self, game: str) -> str:
        sql = "SELECT Description FROM Games WHERE Name = (?)"
        args = [game]
        data = False
        try:
            self.cursor.execute(sql, args)
            data = self.cursor.fetchall()[0][0]
        except:
            print(
                f"Your game {game} does not exist or some other shit happened")
        finally:
            self.conn.commit()
            return data


# setting up the database
def start_database():
    database = "database.db"
    # if no db file -> create one
    if not path.exists(database):
        print("no database found")
        create_path = path.abspath(getcwd())
        create_path = path.join(create_path, database)
        print(f"create_path: {create_path}")
        f = open(create_path, "x")
        f.close()
    else:
        print("Database exist")
    full_path = path.abspath(path.expanduser(path.expandvars(database)))
    DB = DbInterface(full_path)
    return DB


DB = start_database()

if __name__ == "__main__":
    print(DB.get_users())
    print(DB.get_users("PAYED"))
    print(DB.get_users("UNPAYED"))

    # DB.add_user(383327735, 'alexeymarkovski', 'Alexey', 'Markovski', '380952793306')
    # print(DB.check_payed_user(383327735)
