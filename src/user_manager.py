from telegram.ext import CallbackContext

from time import sleep, time
import functools
import threading

from src.data import text


class UserManager:

    def __init__(self):
        self.user_removal_time = 3600
        self.currentUsers = {}
        self.userthread = threading.Thread(target=self.__remove_old_users)
        self.userthread.start()

    def __remove_old_users(self):
        while True:
            sleep(self.user_removal_time)
            print('deleteCycle')
            print(self.currentUsers)
            users_to_delete = []
            for user in self.currentUsers.values():
                if time.time() - user.lastActivityTime > self.user_removal_time:
                    users_to_delete.append(user.chat_id)
            for chat_id in users_to_delete:
                self.delete_user(chat_id)
                print(f'deleting user {chat_id}')

    def delete_user(self, chat_id):
        if chat_id in self.currentUsers:
            del self.currentUsers[chat_id]
        else:
            print(f'[WARNING]DELETING UNEXISTING USER {chat_id}')

    def create_user(self, chat_id):
        self.currentUsers[chat_id] = User(chat_id)

    # Users stored in dictionary with keys as
    # Structure {
    #   user_id: User-class object
    # }


class User:
    def __init__(self, chat_id, Location=None, Type=None, Age=None, Props=None, stage=0):
        self.chat_id = chat_id
        self.Location = Location
        self.Type = Type
        self.Age = Age
        self.Props = Props
        self.stage = stage
        self.lastActivityTime = time()
        self.games = None

    def __str__(self):
        user = f"chat_id: {self.chat_id}\nlocation: {self.Location}\ntype: {self.Type}\nage: {self.Age}\nprops: {self.Props}\nstage: {self.stage}"
        return user

    def get_data(self):
        data = [self.Location, self.Type, self.Age, self.Props]
        return data

    def refresh_action(func):
        def wrapper_refresh_time(self, *args, **kwargs):
            self.update_time()
            value = func(self, *args, **kwargs)
            return value

        return wrapper_refresh_time

    def update_time(self):
        self.lastActivityTime = time()

    @refresh_action
    def add_location(self, Location, stage):
        if Location == text["outside"]:
            self.Location = "на улице"
        elif Location == text["inside"]:
            self.Location = "дома"
        elif Location == text["trip"]:
            self.Location = "в дороге"
        self.stage = stage
        return Location

    @refresh_action
    def add_type(self, Type, stage):
        if Type == text["active"]:
            self.Type = "активная"
        elif Type == text["educational"]:
            self.Type = "обучающая"
        elif Type == text["calming"]:
            self.Type = "успокаивающая"
        elif Type == text["family"]:
            self.Type = "семейная"
        elif Type == text["task"]:
            self.Type = "сам"
        self.stage = stage
        return Type

    @refresh_action
    def add_age(self, Age, stage):
        if Age == text["2-3"]:
            self.Age = "2-3"
        elif Age == text["3-4"]:
            self.Age = "3-4"
        elif Age == text["4-6"]:
            self.Age = "4-6"
        elif Age == text["6-8"]:
            self.Age = "6-8"
        self.stage = stage
        return Age

    @refresh_action
    def add_props(self, Props, stage):
        if Props == text["yes"]:
            self.Props = "да"
        elif Props == text["no"]:
            self.Props = "нет"
        self.stage = stage
        return Props

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
