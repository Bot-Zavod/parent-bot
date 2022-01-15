import logging
import os

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from bot.data import text
from bot.database import db_interface
from bot.states import State


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# save chat_id to users.txt in case it is not already there
# def save_id(chat_id):
#     path = "users.txt"
#     full_path = os.path.abspath(os.path.expanduser(
#         os.path.expandvars(path)))

#     with open(full_path, 'r+') as users:
#         chat_id = str(chat_id)+"\n"
#         if chat_id not in users.read():
#             users.write(chat_id)
#         else:
#             print("This fucker is already here")
#         users.close()


def start(update, context):
    chat_id = update.message.chat.id
    logger.info("User %s: send /start command;", chat_id)
    db_interface.save_id(chat_id)
    reply_keyboard = [[text["games"]]]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["start_games"], reply_markup=reply_markup)
    return State.ASK_LOCATION


def stop_bot(update, context):
    update.message.reply_text(text["stop"])
    logger.info("User %s: finished ConversationHandler;", update.message.chat.id)
    return ConversationHandler.END


def terms(update, context):
    update.message.reply_text(text=text["terms"])
    logger.info("User %s: ask Terms;", update.message.chat.id)


def error(update, context):
    """Log Errors caused by Updates."""
    update = 0
    logger.warning('Update "%s" caused error "%s"', update, context.error)
