from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from database import DbInterface
from os import getcwd, environ
from user import UserManager
from random import randint
from etc import text
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text(text["start"], reply_markup = ReplyKeyboardRemove())
    pass


def done(update, context):
    update.message.reply_text('END')
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def get_games_id(update,context):
	db = DbInterface(getcwd() + "/database.db")
	UM = UserManager()
    answer = UM.currentUsers[update.message.chat.id].answers
    game_id = []
    game_id += db.getGames(answer[0],answer[1],answer[2],answer[3],answer[4])

    if None in answer:
        keys = [[0,1,2],[0,1],[0,1,2],[0,1],[0,1]]
        data = [answer[0],answer[1],answer[2],answer[3],answer[4]]
        for j in range(5):
            if answer[j] == None:
                for i in keys[j]:
                    data[j] = i
                    game_id += db.getGames(*data)
        game_id = sorted(list(set(game_id)))
    
    return game_id


def start_query(update, context):
    reply_keyboard = [[text["games"]],[text["random"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["start_games"], reply_markup = markup)
    return GAMES


def game_start(update,context):
    if update.message.text == text["games"]:
        return a_type(update,context)
    elif update.message.text == text["random"]:
        return rand(update,context)


def rand(update,context):
    reply_keyboard = [[text["back"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(games[randint(1,53)], reply_markup = markup)
    return BACK


def back(update,context):
    if update.message.text == text["back"]:
        return start_query(update, context)


def back_answer(update,context):
    massage = update.message.text
    lang = UM.currentUsers[update.message.chat.id].lang
    if massage == text["back"]:
        return result(update,context)
    elif massage == text["menu"]:
        return start_query(update, context)