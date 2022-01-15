from telegram import ReplyKeyboardMarkup

from bot.data import text
from bot.states import State


# def get_games_id(update,context):
# 	db = DbInterface(getcwd() + "/database.db")
# 	UM = UserManager()
#     # answer = UM.current_users[update.message.chat.id]
#     game_id = []
#     game_id += db.getGames(answer[0],answer[1],answer[2],answer[3],answer[4])

#     if None in answer:
#         keys = [[0,1,2],[0,1],[0,1,2],[0,1],[0,1]]
#         data = [answer[0],answer[1],answer[2],answer[3],answer[4]]
#         for j in range(5):
#             if answer[j] == None:
#                 for i in keys[j]:
#                     data[j] = i
#                     game_id += db.getGames(*data)
#         game_id = sorted(list(set(game_id)))

#     return game_id


def start_query(update, context):
    reply_keyboard = [[text["games"]], [text["random"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["start_games"], reply_markup=markup)
    return State.GAMES


def back(update, context):
    if update.message.text == text["back"]:
        return start_query(update, context)
