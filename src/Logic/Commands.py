from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from os import getcwd
import logging

from database import DbInterface
from variables import *
from etc import text


logging.basicConfig(format='%(asctime)s - %(name)s - \
                                %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


path = getcwd() + "/database.db"
db = DbInterface(path = path)

def start(update, context):
    isPayed = db.checkUser(update.message.chat.id)
    if isPayed:
        update.message.reply_text("fuck you")
    else:
        reply_keyboard = [[text["pay_please"]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text(text["start"], reply_markup = markup)
        return PAY

def done(update, context):
    update.message.reply_text('END')
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)