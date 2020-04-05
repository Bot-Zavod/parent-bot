from telegram import ReplyKeyboardRemove
from Entities.etc import text
from os import getcwd
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text(text["start"], reply_markup = ReplyKeyboardRemove())
    pass