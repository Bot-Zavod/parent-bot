from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler
from os import getcwd
import logging

from .database import DB
from .variables import *
from .etc import text
from .Payment import subscribe


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    chat_id = update.message.chat.id

    # check if user is already in DB, if not add him
    if not DB.check_user(chat_id):
        DB.add_user(chat_id)
    
    # check if user has payed already
    isPayed = DB.check_payed_user(chat_id)
    if isPayed:
        reply_keyboard = [[text["games"]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("Поиграй со своим малым! Вот игры...", reply_markup = markup)
        return ASK_LOCATION
    else:
        # text = "Привет дорогой друг! Вы можете глянуть демо игры или купить подписку!"
        demo_button = InlineKeyboardButton("Демо игры 🎲", callback_data = "demo")
        subscribe_button = InlineKeyboardButton("Оформить подписку ✅", callback_data = "subscribe")
        reply_markup = InlineKeyboardMarkup([[demo_button],[subscribe_button]])
        update.message.reply_text(text="text", reply_markup=reply_markup)

    logger.info("User %s: send /start command;", update.message.chat.id)

def demo(update, context):
    text = "После подписки ты сможешь увидеть игры на подобии этих..."
    subscribe_button = InlineKeyboardButton("Оформить подписку ✅", callback_data = "subscribe")
    reply_markup = InlineKeyboardMarkup([[subscribe_button]])
    context.bot.edit_message_text(
        chat_id = update.callback_query.message.chat.id, 
        message_id = update.callback_query.message.message_id, 
        text="Перейдите по сгенерированной ссылке, для оформления подписки", 
        reply_markup=reply_markup
        )
    logger.info("User %s: ask DEMO games;", update.callback_query.message.chat.id)

def done(update, context):
    update.message.reply_text('END')
    logger.info("User %s: finished ConversationHandler;", update.message.chat.id)
    return ConversationHandler.END

def terms(update, context):
    update.message.reply_text(text=text["terms"])
    logger.info("User %s: ask Terms;", update.message.chat.id)


def error(update, context):
    """Log Errors caused by Updates."""
    update = 0
    logger.warning('Update "%s" caused error "%s"', update, context.error)