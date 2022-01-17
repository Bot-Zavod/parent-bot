import os
from functools import wraps
from random import choice
from typing import List
from typing import Tuple

from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext

from bot.data import emoji
from bot.data import photos
from bot.data import text
from bot.database import db_interface
from bot.handlers.base import start
from bot.states import State
from bot.user_manager import user_manager
from bot.utils.log import log_message


def check_state(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        if chat_id not in user_manager.current_users:
            return start(update, context)
        return func(update, context)

    return wrapper


def send_message_with_keyboard(msg: str, keyboard: list, update: Update):
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(text=msg, reply_markup=markup)


def get_id_msg(update: Update) -> Tuple[int, str]:
    chat_id = update.message.chat.id
    massage = update.message.text
    return chat_id, massage


def ask_location(update: Update, context: CallbackContext):
    log_message(update)
    chat_id = update.message.chat.id
    user_manager.create_user(chat_id)
    keyboard = [
        [text["inside"]],
        [text["outside"]],
        [text["trip"]],
        [text["back"]],
    ]
    send_message_with_keyboard(text["ask_location"], keyboard, update)
    return State.GET_LOCATION


@check_state
def get_location(update: Update, context: CallbackContext):
    log_message(update)
    chat_id, massage = get_id_msg(update)
    user_manager.current_users[chat_id].add_location(massage)
    return ask_type(update, context)


def ask_type(update: Update, context: CallbackContext):
    log_message(update)
    keyboard = [
        [text["active"], text["educational"]],
        [text["calming"]],
        [text["family"], text["task"]],
        [text["back"]],
    ]
    if update.message.text == text["outside"]:
        keyboard.pop(2)  # skip family and task

    send_message_with_keyboard(text["ask_type"], keyboard, update)
    return State.GET_TYPE


@check_state
def get_type(update: Update, context: CallbackContext):
    log_message(update)
    chat_id, massage = get_id_msg(update)
    user_manager.current_users[chat_id].add_type(massage)
    if massage == text["family"]:  # skip age question
        return ask_props(update, context)
    return ask_age(update, context)


def ask_age(update: Update, context: CallbackContext):
    keyboard = [
        [text["2-3"], text["3-4"]],
        [text["4-6"], text["6-8"]],
        [text["back"]],
    ]

    send_message_with_keyboard(text["ask_age"], keyboard, update)
    return State.GET_AGE


@check_state
def get_age(update: Update, context: CallbackContext):
    log_message(update)
    chat_id, massage = get_id_msg(update)
    user_manager.current_users[chat_id].add_age(massage)
    return ask_props(update, context)


def ask_props(update: Update, context: CallbackContext):
    keyboard = [[text["yes"]], [text["no"]], [text["back"]]]
    send_message_with_keyboard(text["ask_props"], keyboard, update)
    return State.GET_PROPS


@check_state
def get_props(update: Update, context: CallbackContext):
    log_message(update)
    chat_id, massage = get_id_msg(update)
    user_manager.current_users[chat_id].add_props(massage)
    return ask_games(update, context)


@check_state
def ask_games(update: Update, context: CallbackContext):
    """search games or retrive from cache"""
    chat_id = update.message.chat.id

    if user_manager.current_users[chat_id].games:
        reply_keys = user_manager.current_users[chat_id].games
    else:  # generate games
        user_query = user_manager.current_users[chat_id].get_data()
        user_games = db_interface.get_games(user_query)

        reply_keys = [[name[0]] for name in user_games]
        user_manager.current_users[chat_id].games = reply_keys[:]  # cache keys copy

    msg_text = text["ask_games" if reply_keys else "no_result"]

    def add_emoji(key: List[str]) -> List[str]:
        return [key[0] + " " + choice(emoji)]

    keyboard = list(map(add_emoji, reply_keys))
    keyboard += [text["back"], text["menu"]]

    send_message_with_keyboard(msg_text, keyboard, update)
    return State.GET_GAME


def get_games(update: Update, context: CallbackContext):
    massage = update.message.text
    chat_id = update.message.chat.id

    game = massage[:-2].strip()  # remove emoji
    if [game] not in user_manager.current_users[chat_id].games:
        return State.GET_GAME  # igmore non games keys

    game_desc = db_interface.get_game(game)

    if game in photos.keys():  # send img if exist
        img_path = os.path.join("images", photos[game])
        update.message.reply_photo(photo=open(img_path, "rb"), caption=game)

    game_desc = game_desc.replace("<br>", "\n")
    keyboard = [[text["back"], text["menu"]]]

    send_message_with_keyboard(game_desc, keyboard, update)
    return State.BACK_ANSWER
