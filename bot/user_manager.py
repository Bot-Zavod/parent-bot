import threading
import time

from bot.data import text


class UserManager:
    def __init__(self):
        self.user_removal_time = 3600
        self.current_users = {}
        self.userthread = threading.Thread(target=self.__remove_old_users)
        self.userthread.start()

    def __remove_old_users(self):
        while True:
            time.sleep(self.user_removal_time)
            print("deleteCycle")
            print(self.current_users)
            users_to_delete = []
            for user in self.current_users.values():
                if time.time() - user.last_activity_time > self.user_removal_time:
                    users_to_delete.append(user.chat_id)
            for chat_id in users_to_delete:
                self.delete_user(chat_id)
                print(f"deleting user {chat_id}")

    def delete_user(self, chat_id):
        if chat_id in self.current_users:
            del self.current_users[chat_id]
        else:
            print(f"[WARNING]DELETING UNEXISTING USER {chat_id}")

    def create_user(self, chat_id):
        self.current_users[chat_id] = User(chat_id)

    # Users stored in dictionary with keys as
    # Structure {
    #   user_id: User-class object
    # }


def refresh_action(func):
    def wrapper_refresh_time(self, *args, **kwargs):
        self.update_time()
        value = func(self, *args, **kwargs)
        return value

    return wrapper_refresh_time


class User:
    def __init__(
        self, chat_id, location=None, game_type=None, age=None, props=None, stage=0
    ):
        self.chat_id = chat_id
        self.location = location
        self.game_type = game_type
        self.age = age
        self.props = props
        self.stage = stage
        self.last_activity_time = time.time()
        self.games = None

    def __str__(self):
        user = f"chat_id: {self.chat_id}\nlocation: {self.location}\ntype: {self.game_type}\nage: {self.age}\nprops: {self.props}\nstage: {self.stage}"
        return user

    def get_data(self):
        data = [self.location, self.game_type, self.age, self.props]
        return data

    def update_time(self):
        self.last_activity_time = time.time()

    @refresh_action
    def add_location(self, location, stage):
        if location == text["outside"]:
            self.location = "на улице"
        elif location == text["inside"]:
            self.location = "дома"
        elif location == text["trip"]:
            self.location = "в дороге"
        self.stage = stage
        return location

    @refresh_action
    def add_type(self, game_type, stage):
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
        self.stage = stage
        return game_type

    @refresh_action
    def add_age(self, age, stage):
        if age == text["2-3"]:
            self.age = "2-3"
        elif age == text["3-4"]:
            self.age = "3-4"
        elif age == text["4-6"]:
            self.age = "4-6"
        elif age == text["6-8"]:
            self.age = "6-8"
        self.stage = stage
        return age

    @refresh_action
    def add_props(self, props, stage):
        if props == text["yes"]:
            self.props = "да"
        elif props == text["no"]:
            self.props = "нет"
        self.stage = stage
        return props

    @refresh_action
    def add_games(self, games):
        self.games = games
        return games


UM = UserManager()
# if __name__ == "__main__":
#     user = User(100500)
#     user.addQuestions([1,2,3,4,5])
#     user.addAnswer(1, 0)
#     print(user.answers)
