from functools import wraps

from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext

from bot.admins import ADMINS
from bot.data import text
from bot.database import db_interface
from bot.states import State
from bot.utils.log import log_message
from bot.utils.spreadsheet import update_games

PUSH_TEXT = None  # for text that admin wants to send


def restrict_user(func):
    """checks if you are a true admin"""

    @wraps(func)
    def wrapper(update: Update, context: CallbackContext):
        if update.message.chat.id in ADMINS:
            return func(update, context)
        update.message.reply_text(text["options_admin"]["not_boss"])
        return None

    return wrapper


@restrict_user
def admin_menu(update: Update, context: CallbackContext):
    """show up basic admin menu"""

    reply_keyboard = [
        [text["options_admin"]["push"], text["options_admin"]["users"]],
        [text["options_admin"]["update_games"]],
        [text["back"]],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(
        text=text["options_admin"]["hi_boss"], reply_markup=markup
    )
    return State.ADMIN


@restrict_user
def update_games_tables(update: Update, context: CallbackContext):
    games_num = update_games()
    msg = f"Games database was succesfully updated with {games_num} games"
    update.message.reply_text(text=msg)
    return State.ADMIN


@restrict_user
def list_users(update: Update, context: CallbackContext):
    users_count = db_interface.users_count()
    msg = f"Воспользовались: {users_count}"
    update.message.reply_text(text=msg)
    return State.ADMIN


@restrict_user
def ask_push_text(update: Update, context: CallbackContext):
    update.message.reply_text(text=text["options_admin"]["ask_push_text"])
    return State.PUSH_WHAT


@restrict_user
def set_push_text(update: Update, context: CallbackContext):
    """catches admin massage"""
    global PUSH_TEXT
    answer = update.message.text
    PUSH_TEXT = answer

    reply_keyboard = [[text["options_admin"]["send"], text["options_admin"]["no_send"]]]
    markup = ReplyKeyboardMarkup(
        reply_keyboard, resize_keyboard=True, one_time_keyboard=True
    )
    msg = text["options_admin"]["push_submit"].format(answer=answer)
    update.message.reply_text(text=msg, reply_markup=markup)
    return State.PUSH_SUBMIT


@restrict_user
def push_handler(update: Update, context: CallbackContext):
    log_message(update)
    global PUSH_TEXT
    # sending the notification message
    users_ids = db_interface.get_users()
    for chat_id in users_ids:
        context.bot.send_message(chat_id=chat_id, text=PUSH_TEXT)
    user_number = len(users_ids)
    update.message.reply_text(
        text=text["options_admin"]["push_success"].format(user_number=user_number)
    )
    return admin_menu(update, context)
