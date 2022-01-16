import os
from functools import wraps
from random import choice

from telegram import ParseMode
from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext

from bot.data import emoji
from bot.data import photos
from bot.data import text
from bot.database import db_interface
from bot.handlers.base import start
from bot.states import State
from bot.user_manager import UM


def check_state(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        if chat_id not in UM.current_users:
            return start(update, context)
        return func(update, context)

    return wrapper


def ask_location(update: Update, context: CallbackContext):
    massage = update.message.text
    if massage == text["games"]:
        UM.create_user(update.message.chat.id)
    elif massage == text["back"]:
        pass
    else:
        UM.delete_user(update.message.chat.id)
        return start(update, context)

    reply_keyboard = [
        [text["inside"]],
        [text["outside"]],
        [text["trip"]],
        [text["back"]],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_location"], reply_markup=markup)
    return State.ASK_TYPE


@check_state
def ask_type(update: Update, context: CallbackContext):
    massage = update.message.text
    chat_id = update.message.chat.id

    if massage in (text["inside"], text["outside"], text["trip"]):
        UM.current_users[chat_id].add_location(massage, 1)
    elif massage == text["back"]:
        if UM.current_users[chat_id].stage == 0:
            UM.delete_user(update.message.chat.id)
            return start(update, context)
    else:
        return start(update, context)

    reply_keyboard = [
        [text["active"]],
        [text["educational"]],
        [text["calming"]],
        [text["family"]],
        [text["task"]],
        [text["back"]],
    ]
    if massage == text["outside"]:
        reply_keyboard = reply_keyboard[:3] + [reply_keyboard[-1]]
    elif massage == text["trip"]:
        return ask_age(update, context)
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_type"], reply_markup=markup)
    return State.ASK_AGE


@check_state
def ask_age(update: Update, context: CallbackContext):
    massage = update.message.text
    chat_id = update.message.chat.id

    if massage in (
        text["active"],
        text["educational"],
        text["calming"],
        text["family"],
        text["task"],
    ):
        UM.current_users[chat_id].add_type(massage, 2)
    elif massage == text["back"]:
        if UM.current_users[chat_id].stage == 1:
            UM.current_users[chat_id].stage = 0
            return ask_location(update, context)
    elif massage == text["trip"]:
        pass
    else:
        return ask_location(update, context)

    if massage == text["family"]:
        print(UM.current_users[chat_id])
        return ask_props(update, context)

    reply_keyboard = [
        [text["2-3"]],
        [text["3-4"]],
        [text["4-6"]],
        [text["6-8"]],
        [text["back"]],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_age"], reply_markup=markup)
    return State.ASK_PROPS


@check_state
def ask_props(update: Update, context: CallbackContext):
    massage = update.message.text
    chat_id = update.message.chat.id

    if massage in (text["2-3"], text["3-4"], text["4-6"], text["6-8"]):
        UM.current_users[chat_id].add_age(massage, 3)
    elif massage == text["family"]:
        pass
    elif massage == text["back"]:
        if UM.current_users[chat_id].stage == 2:
            UM.current_users[chat_id].stage = 1
            return ask_type(update, context)
    else:
        return ask_type(update, context)

    reply_keyboard = [[text["yes"]], [text["no"]], [text["back"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_props"], reply_markup=markup)
    return State.RESULT


def result(update: Update, context: CallbackContext):
    massage = update.message.text
    chat_id = update.message.chat.id

    if massage not in (text["yes"], text["no"], text["back"]):
        return ask_age(update, context)

    if massage in (text["yes"], text["no"]):
        UM.current_users[chat_id].add_props(massage, 4)
    else:
        if UM.current_users[chat_id].stage == 3:
            UM.current_users[chat_id].stage = 2
            return ask_age(update, context)
        elif UM.current_users[chat_id].stage == 1:
            UM.current_users[chat_id].stage = 0
            return ask_type(update, context)
        elif UM.current_users[chat_id].stage == 2:
            return ask_age(update, context)

    print(UM.current_users[chat_id])
    if UM.current_users[chat_id].games is None:
        user_data = UM.current_users[chat_id].get_data()
        user_games = db_interface.get_games(*user_data)
        reply_keys = [[name[0]] for name in user_games]
        UM.current_users[chat_id].add_games(reply_keys[:])
    else:
        reply_keys = UM.current_users[chat_id].games

    if reply_keys is None:
        answer = text["no_result"]
    else:
        answer = text["result"]

    reply_keyboard = list(map(lambda x: [x[0] + " " + choice(emoji)], reply_keys)) + [
        [text["menu"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text=answer, reply_markup=markup)
    return State.ANSWER


def final_answer(update: Update, context: CallbackContext):
    massage = update.message.text
    chat_id = update.message.chat.id

    if massage == text["menu"]:
        UM.delete_user(chat_id)
        return start(update, context)
    UM.current_users[chat_id].stage = 5

    # print(UM.current_users[chat_id].games)
    game = massage[:-2].strip()
    if [game] in UM.current_users[chat_id].games:
        description = db_interface.get_game(game)
        # print(description)
    else:
        print(f"\n{game}\n")
        return result(update, context)

    if game in photos.keys():
        img_path = os.path.join("images", photos[game])
        update.message.reply_photo(photo=open(img_path, "rb"), caption=game)

    reply_keyboard = [[text["back"], text["menu"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(
        text=description.replace("<br>", "\n"),
        reply_markup=markup,
        parse_mode=ParseMode.HTML,
    )
    return State.BACK_ANSWER


def back_answer(update: Update, context: CallbackContext):
    massage = update.message.text
    chat_id = update.message.chat.id
    if massage == text["back"]:
        return result(update, context)
    elif massage == text["menu"]:
        UM.delete_user(chat_id)
        return start(update, context)
