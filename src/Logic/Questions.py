from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from .user_manager import UM
from .database import DB
from .Commands import start
from .variables import *
from .etc import text, photos

def check(chat_id, update, context):
    if chat_id not in UM.currentUsers:
        return start(update,context)


def ask_location(update,context):
    massage = update.message.text
    if massage == text["games"]:
        UM.create_user(update.message.chat.id)
    elif massage == text["back"]:
        pass
    else:
        UM.delete_user(update.message.chat.id)
        return start(update,context)

    reply_keyboard = [[text["inside"]],
                      [text["outside"]],
                      [text["trip"]],
                      [text["back"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_location"], reply_markup = markup)
    return ASK_TYPE

def ask_type(update,context):
    massage = update.message.text
    chat_id = update.message.chat.id
    check(chat_id, update, context)

    if massage in (text["inside"], text["outside"], text["trip"]):
        UM.currentUsers[chat_id].add_location(massage, 1)
    elif massage == text["back"]:
        if UM.currentUsers[chat_id].stage == 0:
            UM.delete_user(update.message.chat.id)
            return start(update,context)
    else:
        return start(update,context)

    reply_keyboard = [[text["active"]],
                      [text["educational"]],
                      [text["calming"]],
                      [text["family"]],
                      [text["task"]],
                      [text["back"]]]
    if massage == text["outside"]:
        reply_keyboard = reply_keyboard[:3] + [reply_keyboard[-1]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_type"], reply_markup = markup)
    return ASK_AGE

def ask_age(update,context):
    massage = update.message.text
    chat_id = update.message.chat.id
    check(chat_id, update, context)

    if massage in (text["active"], text["educational"], text["calming"], \
                    text["family"], text["task"]):
        UM.currentUsers[chat_id].add_type(massage, 2)
    elif massage == text["back"]:
        if UM.currentUsers[chat_id].stage == 1:
            UM.currentUsers[chat_id].stage = 0
            return ask_location(update,context)
    elif massage == text["trip"]:
        pass
    else:
        return ask_location(update,context)

    if massage == text["family"]:
        print(UM.currentUsers[chat_id])
        return ask_props(update,context)

    reply_keyboard = [[text["2-3"]],
                      [text["3-4"]],
                      [text["4-6"]],
                      [text["6-8"]],
                      [text["back"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_age"], reply_markup = markup)
    return ASK_PROPS

def ask_props(update,context):
    massage = update.message.text
    chat_id = update.message.chat.id
    check(chat_id, update, context)

    if massage in (text["2-3"], text["3-4"], text["4-6"], text["6-8"]):
        UM.currentUsers[chat_id].add_age(massage, 3)
    elif massage == text["family"]:
        pass
    elif massage == text["back"]:
        if UM.currentUsers[chat_id].stage == 2:
            UM.currentUsers[chat_id].stage = 1
            return ask_type(update,context)
    else:
        return ask_type(update,context)

    reply_keyboard = [[text["yes"]],
                      [text["no"]],
                      [text["back"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_props"], reply_markup = markup)
    return RESULT

def result(update,context):
    massage = update.message.text
    chat_id = update.message.chat.id
    check(chat_id, update, context)

    if massage in (text["yes"], text["no"]):
        UM.currentUsers[chat_id].add_props(massage, 4)
    elif massage == text["back"]:
        if UM.currentUsers[chat_id].stage == 3:
            UM.currentUsers[chat_id].stage = 2
            return ask_age(update,context)
        elif UM.currentUsers[chat_id].stage == 1:
            UM.currentUsers[chat_id].stage = 0
            return ask_type(update,context)
        elif UM.currentUsers[chat_id].stage == 2:
            return ask_age(update,context)
    else:
        return ask_age(update,context)

    print(UM.currentUsers[chat_id])
    if UM.currentUsers[chat_id].games == None:
        user_data = UM.currentUsers[chat_id].get_data()
        user_games = DB.get_games(*user_data)
        reply_keys = [[name[0]] for name in user_games]
        UM.currentUsers[chat_id].add_games(reply_keys[:])
    else:
        reply_keys = UM.currentUsers[chat_id].games
    
    if reply_keys == None:
        answer = text["no_result"]
    else:
        answer = text["result"]
    reply_keyboard = reply_keys + [[text["back"],text["menu"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text = answer, reply_markup = markup)
    return ANSWER

def final_answer(update,context):
    massage = update.message.text
    chat_id = update.message.chat.id
    check(chat_id, update, context)

    if massage == text["back"] and \
            UM.currentUsers[chat_id].stage == 4:

        return result(update,context)
    elif massage == text["menu"]:
        UM.delete_user(chat_id)
        return start(update, context)
    UM.currentUsers[chat_id].stage = 5

    # print(UM.currentUsers[chat_id].games)
    game = massage
    if [game] in UM.currentUsers[chat_id].games:
        description = DB.get_game(game)
        print(description)
    else:
        return result(update,context)

    # if relative pfoto exists -> send it
    if game in photos.keys():
        update.message.reply_photo(photo=open(f"img/{photos[game]}", 'rb'), caption = game)

    reply_keyboard = [[text["back"],text["menu"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text = description, reply_markup = markup)
    return BACK_ANSWER

def back_answer(update,context):
    massage = update.message.text
    chat_id = update.message.chat.id
    check(chat_id, update, context)

    if massage == text["back"]:
        return result(update,context)
    elif massage == text["menu"]:
        UM.delete_user(chat_id)
        return start(update, context)