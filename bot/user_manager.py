import time
from typing import Dict
from typing import NamedTuple

from loguru import logger

from bot.data import text


class UserManager:
    def __init__(self):
        self.user_removal_time: int = 60 * 60  # seconds
        self.current_users: Dict[int, User] = {}

    def remove_old_users(self, *args, **kwargs):
        """Clear cache of results which have timed out"""
        # args and kwargs need for calling it in job_queue
        users_to_delete = []
        for user in self.current_users.values():
            if time.time() - user.last_activity_time > self.user_removal_time:
                users_to_delete.append(user.chat_id)
        for chat_id in users_to_delete:
            self.delete_user(chat_id)

    def delete_user(self, chat_id: int):
        try:
            del self.current_users[chat_id]
        except KeyError:
            logger.warning(f"DELETING UNEXISTING USER {chat_id}")

    def create_user(self, chat_id):
        self.current_users[chat_id] = User(chat_id)


def refresh_action(func):
    def wrapper_refresh_time(self, *args, **kwargs):
        self.update_time()
        value = func(self, *args, **kwargs)
        return value

    return wrapper_refresh_time


class UserQuery(NamedTuple):
    location: str
    game_type: str
    age: str
    props: str


class User:
    def __init__(self, chat_id, location=None, game_type=None, age=None, props=None):
        self.chat_id = chat_id
        self.location = location
        self.game_type = game_type
        self.age = age
        self.props = props
        self.last_activity_time = time.time()
        self.games = None

    def __str__(self):
        user = f"chat_id: {self.chat_id}\nlocation: {self.location}\ntype: {self.game_type}\nage: {self.age}\nprops: {self.props}"
        return user

    def get_data(self) -> UserQuery:
        return UserQuery(
            location=self.location,
            game_type=self.game_type,
            age=self.age,
            props=self.props,
        )

    def update_time(self):
        self.last_activity_time = time.time()

    @refresh_action
    def add_location(self, location: str):
        if location == text["outside"]:
            self.location = "на улице"
        elif location == text["inside"]:
            self.location = "дома"
        elif location == text["trip"]:
            self.location = "в дороге"
        return location

    @refresh_action
    def add_type(self, game_type: str):
        if game_type == text["active"]:
            self.game_type = "активная"
        elif game_type == text["educational"]:
            self.game_type = "обучающая"
        elif game_type == text["calming"]:
            self.game_type = "успокаивающая"
        elif game_type == text["family"]:
            self.game_type = "семейная"
        elif game_type == text["task"]:
            self.game_type = "сам"
        return game_type

    @refresh_action
    def add_age(self, age: str):
        if age == text["2-3"]:
            self.age = "2-3"
        elif age == text["3-4"]:
            self.age = "3-4"
        elif age == text["4-6"]:
            self.age = "4-6"
        elif age == text["6-8"]:
            self.age = "6-8"
        return age

    @refresh_action
    def add_props(self, props: str):
        if props == text["yes"]:
            self.props = "да"
        elif props == text["no"]:
            self.props = "нет"
        return props

    @refresh_action
    def add_games(self, games):
        self.games = games
        return games


user_manager = UserManager()
