import os
from datetime import timedelta

from dotenv import load_dotenv
from loguru import logger
from telegram import Bot
from telegram import ParseMode
from telegram.ext import CommandHandler
from telegram.ext import Defaults
from telegram.ext import PicklePersistence
from telegram.ext import Updater

from bot.commands import clear_bot
from bot.commands import set_bot_commands
from bot.conv_handler import conv_handler
from bot.handlers.base import error_handler
from bot.handlers.base import terms
from bot.user_manager import user_manager


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
    bot_token = os.getenv("BOT_TOKEN")
    setup_bot(bot_token)
    main_dir = os.path.dirname(os.path.dirname(__file__))
    storage_path = os.path.join(main_dir, "storage.pickle")
    my_persistence = PicklePersistence(filename=storage_path)
    defaults = Defaults(parse_mode=ParseMode.HTML)

    updater = Updater(
        token=bot_token,
        persistence=my_persistence,
        use_context=True,
        defaults=defaults,
        workers=6,
    )

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("info", terms))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error_handler)

    job = updater.job_queue

    job.run_repeating(
        callback=user_manager.remove_old_users,
        interval=timedelta(hours=1),
        first=0,
        name="local cache",
    )

    updater.start_polling()
    logger.debug("Bot launched succesfully")
    updater.idle()


if __name__ == "__main__":
    main()
