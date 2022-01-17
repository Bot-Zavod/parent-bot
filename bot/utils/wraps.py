from functools import wraps

from telegram import Update
from telegram.ext import CallbackContext

from bot.admins import ADMINS
from bot.data import text
from bot.handlers.base import start
from bot.user_manager import user_manager


def check_state(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        if chat_id not in user_manager.current_users:
            return start(update, context)
        return func(update, context)

    return wrapper


def restrict_user(func):
    """checks if you are a true admin"""

    @wraps(func)
    def wrapper(update: Update, context: CallbackContext):
        if update.message.chat.id in ADMINS:
            return func(update, context)
        update.message.reply_text(text["not_boss"])
        return None

    return wrapper
