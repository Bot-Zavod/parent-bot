import contextlib
import os
import sqlite3
from typing import List
from typing import Optional

from loguru import logger

from bot.user_manager import UserQuery


class DbInterface:
    def __init__(self, path: str):
        self.db_path = path
        self.create_tables()

    def create_tables(self) -> None:
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
            self.query([sql])

    def query(
        self,
        statement: list,
        fetch: bool = False,
        executemany: bool = False,
    ) -> Optional[list]:
        data = None
        try:
            with contextlib.closing(
                sqlite3.connect(self.db_path, check_same_thread=False)
            ) as conn:  # auto-closes
                with conn:  # auto-commits
                    with contextlib.closing(conn.cursor()) as cursor:  # auto-closes
                        if executemany:
                            cursor.executemany(*statement)
                        else:
                            cursor.execute(*statement)
                        if fetch:
                            data = cursor.fetchall()
        except Exception as error:
            sql = statement[0]
            args = statement[1] if len(statement) == 2 else []
            logger.error(
                f"Failed to execute '{sql}' with args '{args}' because of exception:\n{error}"
            )
            raise Exception from error
        return data

    # ==========
    # USERS
    # ==========

    def save_id(self, chat_id) -> None:
        """save id to Users"""
        sql = "INSERT OR IGNORE INTO Users (chat_id) values(?)"
        args = [chat_id]
        self.query([sql, args])

    def users_count(self) -> int:
        """return number of visitors"""
        sql = "SELECT COUNT(*) FROM Users"
        users = self.query([sql], fetch=True)
        users_count = users[0][0]  # type: ignore
        return users_count

    def get_users(self) -> list:
        """return chat_id list of passed user category"""
        sql = "SELECT chat_id FROM Users"
        answer = self.query([sql], fetch=True)
        users = answer[0]  # type: ignore
        return users

    # ===========
    # GAMES
    # ===========

    def delete_games(self) -> None:
        """cleans games table before update"""
        sql = "DELETE FROM Games"
        self.query([sql])

    def set_games(self, games_to_insert: List[list]) -> None:
        """insert multiple games to the database at once"""
        sql = "INSERT INTO Games (Name, description, location, game_type, age, props) VALUES (?,?,?,?,?,?)"
        self.query([sql, games_to_insert], executemany=True)

    def get_games(self, user_query: UserQuery) -> Optional[list]:
        """return all games+name that sutisfy the qequirments"""
        sql = "SELECT Name, description FROM Games WHERE "
        sql += f"(location LIKE '%{user_query.location}%' OR location=\"\")"
        if user_query.age is not None:
            sql += f"AND (age LIKE '%{user_query.age}%' OR age=\"\")"
        if user_query.game_type is not None:
            sql += f"AND (game_type LIKE '%{user_query.game_type}%' OR game_type=\"\")"
        if user_query.props is not None:
            sql += f"AND (props LIKE '%{user_query.props}%' OR props=\"\")"

        data = self.query([sql], fetch=True)
        return data

    def get_game(self, game: str) -> str:
        """return game with a passed name"""
        sql = "SELECT description FROM Games WHERE Name = (?)"
        args = [game]
        game = self.query([sql, args], fetch=True)  # type: ignore
        data = game[0][0]
        return data


def start_database() -> DbInterface:
    """setting up the database"""
    database = "db.sqlite3"
    # if no db file -> create one
    if not os.path.exists(database):
        logger.info(f"No database '{database}' found")
        create_path = os.path.abspath(os.getcwd())
        create_path = os.path.join(create_path, database)
        logger.info(f"Create path: {create_path}")
        file = open(create_path, "x")
        file.close()
    else:
        logger.info(f"Database '{database}' exist")
    full_path = os.path.abspath(os.path.expanduser(os.path.expandvars(database)))
    interface = DbInterface(full_path)
    return interface


db_interface = start_database()

if __name__ == "__main__":
    # db_interface.add_user(383327735, 'alexeymarkovski', 'Alexey', 'Markovski', '380952793306')
    # users = db_interface.get_users()
    # print(users)
    pass
