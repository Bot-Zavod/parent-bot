from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler
from os import getcwd
import logging

from .database import DB
from .variables import *
from .etc import text


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    chat_id = update.message.chat.id
    isPayed = DB.check_payed_user(chat_id)
    # print(f"isPayed: {isPayed}")
    if isPayed:
        reply_keyboard = [[text["games"]]]
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True)
        update.message.reply_text(
            text["start_games"], reply_markup=reply_markup)
        return ASK_LOCATION
    else:
        demo_button = InlineKeyboardButton(
            text["demo_button"], callback_data="demo")
        subscribe_button = InlineKeyboardButton(
            text["subscribe"], callback_data="subscribe")
        reply_markup = InlineKeyboardMarkup(
            [[demo_button], [subscribe_button]])
        update.message.reply_text(
            text=text["pay_please"], reply_markup=reply_markup)

    logger.info("User %s: send /start command;", update.message.chat.id)


def demo(update, context):
    subscribe_button = InlineKeyboardButton(
        text["subscribe"], callback_data="subscribe")
    reply_markup = InlineKeyboardMarkup([[subscribe_button]])
    context.bot.delete_message(
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
    )
    context.bot.send_video(
        chat_id=update.callback_query.message.chat.id,
        video=open("src/Logic/img/demo.mp4", "rb"),
        reply_markup=reply_markup

    )
    logger.info("User %s: ask DEMO games;",
                update.callback_query.message.chat.id)


def done(update, context):
    update.message.reply_text(text["stop"])
    logger.info("User %s: finished ConversationHandler;",
                update.message.chat.id)
    return ConversationHandler.END


def terms(update, context):
    update.message.reply_text(text=text["terms"])
    logger.info("User %s: ask Terms;", update.message.chat.id)


def error(update, context):
    """Log Errors caused by Updates."""
    update = 0
    logger.warning('Update "%s" caused error "%s"', update, context.error)
