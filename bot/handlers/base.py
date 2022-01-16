from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler

from bot.data import text
from bot.database import db_interface
from bot.states import State
from bot.utils.log import log_message


def start(update: Update, context: CallbackContext):
    log_message(update)
    chat_id = update.message.chat.id
    db_interface.save_id(chat_id)
    reply_keyboard = [[text["games"]]]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["start_games"], reply_markup=reply_markup)
    return State.ASK_LOCATION


def stop_bot(update: Update, context: CallbackContext):
    log_message(update)
    update.message.reply_text(text["stop"])
    return ConversationHandler.END


def terms(update: Update, context: CallbackContext):
    log_message(update)
    update.message.reply_text(text=text["terms"])


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    log_message(update)
    print(context.error)
