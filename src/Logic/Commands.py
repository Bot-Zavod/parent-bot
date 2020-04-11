from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler
from os import getcwd
import logging

from database import DbInterface
from variables import *
from etc import text
from Logic.Payment import subscribe


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


db = DbInterface("database.db")

def start(update, context):
    # Тут должна быть функция добавления пользователя в таблицу Users
    # add_user(chat_id, username, first_name, second_name)
    # Функция должна постоянно добавлять нового человека, если есть пропускать

    # Так же надо сделать эту проверку
    # is_pay = db.check_payed_user(update.message.chat.id)
    isPayed = False #fix it!!!!!!
    if isPayed:
        update.message.reply_text("Поиграй со своим малым! Вот игры...")
    else:
        text = "Привет дорогой друг! Вы можете глянуть демо игры или купить подписку!"
        demo_button = InlineKeyboardButton("Демо игры 🎲", callback_data = "demo")
        subscribe_button = InlineKeyboardButton("Оформить подписку ✅", callback_data = "subscribe")
        reply_markup = InlineKeyboardMarkup([[demo_button],[subscribe_button]])
        update.message.reply_text(text=text, reply_markup=reply_markup)

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
    logger.warning('Update "%s" caused error "%s"', update, context.error)