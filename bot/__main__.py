import os

from dotenv import load_dotenv
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from loguru import logger

from bot.admin import admin_handler
from bot.admin import admin_menu
from bot.admin import push_handler
from bot.admin import push_text
from bot.admin import push_who
from bot.commands import start
from bot.commands import stop_bot
from bot.methods import *
from bot.questions import ask_age
from bot.questions import ask_location
from bot.questions import ask_props
from bot.questions import ask_type
from bot.questions import back_answer
from bot.questions import final_answer
from bot.questions import result
from bot.states import State
from bot.conv_handler import conv_handler


logger.add(
    os.path.join("logs", "out.log"),
    rotation="1 week",
    backtrace=True,
    diagnose=True,
    serialize=True,
)
logger.debug("Modules imported succesfully")

load_dotenv()
logger.debug("Enviroment variables loaded")


def setup_bot(bot_token: str):
    """logs data about the bot"""

    bot = Bot(token=bot_token)
    logger.info(f"bot ID: {bot.id}")
    logger.info(f"bot username: {bot.username}")
    logger.info(f"bot link: {bot.link}")

    clear_bot(bot)
    set_bot_commands(bot)


def main():

    token = os.getenv("BOT_TOKEN")
    setup_bot(token)
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("info", terms))

    # dispatcher.add_error_handler(error)
    updater.start_polling()
    logger.debug("Bot launched succesfully")
    updater.idle()


if __name__ == "__main__":
    main()
