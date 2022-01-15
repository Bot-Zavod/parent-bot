import os
import sqlite3
import time


class DbInterface:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        sql_tables = [
            # Games table
            """
            CREATE TABLE IF NOT EXISTS "games" (
            "Name" TEXT,
            "description" TEXT,
            "location" TEXT,
            "age" TEXT,
            "game_type" TEXT,
            "props" TEXT)
            """,
            # Users table
            """
            CREATE TABLE IF NOT EXISTS "users" (
            "chat_id" INTEGER UNIQUE)
            """,
        ]

        for sql in sql_tables:
            self.cursor.execute(sql)
            self.conn.commit()

    def save_id(self, chat_id) -> None:
        """save id to Users"""
        sql = "INSERT OR IGNORE INTO Users (chat_id) values(?)"
        args = [chat_id]
        try:
            self.cursor.execute(sql, args)
        except Exception as error:
            print(f"Saving {chat_id} failed, error: {error}")
        finally:
            self.conn.commit()

    def users_count(self) -> list:
        """return number of [visitors, subscribed, unsubscribed]"""
        sql = "SELECT COUNT(*) FROM Users"
        try:
            self.cursor.execute(sql)
            all_user = self.cursor.fetchall()[0][0]
        except Exception as error:
            print(f"Check failed, error: {error}")
        finally:
            self.conn.commit()

        sql = "SELECT COUNT(*) FROM Payments WHERE status!='unsubscribed'"
        try:
            self.cursor.execute(sql)
            payed_user = self.cursor.fetchall()[0][0]
        except Exception as error:
            print(f"Check failed, error: {error}")
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

        return [all_user, payed_user, all_payed_user - payed_user]

    def get_users(self, group=None) -> list:
        """return chat_id list of passed user category"""
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

    # ================
    # GAMES SECTION
    # =================

    def delete_games(self):
        """cleans games table before update"""
        sql = "DELETE FROM Games"
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(f" Delete shit happened {e}")
        finally:
            self.conn.commit()
        return "Delete done"

    def set_games(self, games_to_insert):
        """insert multiple games to the database at once"""
        sql = "INSERT INTO Games (Name, description, location, game_type, age, props) VALUES (?,?,?,?,?,?)"
        try:
            self.cursor.executemany(sql, games_to_insert)
        except Exception as e:
            print(f"ERROR while inserting {e}")
        finally:
            self.conn.commit()

    def get_games(self, location=None, game_type=None, age=None, props=None):
        """return all games+name that sutisfy the qequirments"""
        sql = "SELECT Name, description FROM Games WHERE "
        sql += f"(location LIKE '%{location}%' OR location=\"\")"
        if age is not None:
            sql += f"AND (age LIKE '%{age}%' OR age=\"\")"
        if game_type is not None:
            sql += f"AND (game_type LIKE '%{game_type}%' OR game_type=\"\")"
        if props is not None:
            sql += f"AND (props LIKE '%{props}%' OR props=\"\")"
        data = []
        try:
            self.cursor.execute(sql)  # , args)
            data = self.cursor.fetchall()
        except:
            print(f"Your request {location, age, game_type, props} failed")
        finally:
            self.conn.commit()
        return data

    def get_game(self, game: str) -> str:
        """return game with a passed name"""
        sql = "SELECT description FROM Games WHERE Name = (?)"
        args = [game]
        data = ""
        try:
            self.cursor.execute(sql, args)
            data = self.cursor.fetchall()[0][0]
        except:
            print(f"Your game {game} does not exist or some other shit happened")
        finally:
            self.conn.commit()
            return data


def start_database():
    """setting up the database"""
    database = "database.db"
    # if no db file -> create one
    if not os.path.exists(database):
        print("no database found")
        create_path = os.path.abspath(os.getcwd())
        create_path = os.path.join(create_path, database)
        print(f"create_path: {create_path}")
        f = open(create_path, "x")
        f.close()
    else:
        print("Database exist")
    full_path = os.path.abspath(os.path.expanduser(os.path.expandvars(database)))
    db_interface = DbInterface(full_path)
    return db_interface


db_interface = start_database()

if __name__ == "__main__":
    print(db_interface.get_users())
    print(db_interface.get_users("PAYED"))
    print(db_interface.get_users("UNPAYED"))

    # db_interface.add_user(383327735, 'alexeymarkovski', 'Alexey', 'Markovski', '380952793306')
    # print(db_interface.check_payed_user(383327735)
