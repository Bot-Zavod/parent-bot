from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from etc import text
from os import getcwd, environ
import logging
from random import randint

from database import DbInterface
from user import UserManager, User
from variables import *
from Logic.Payment import pay, successful_payment_callback, precheckout_callback


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

db = DbInterface(getcwd() + "/database.db")
UM = UserManager()


def get_games_id(update,context):
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



def start(update, context):
    update.message.reply_text(text["start"], reply_markup = ReplyKeyboardRemove())
    pass


def admin(update, context):
    pass


def done(update, context):
    update.message.reply_text('END')
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(environ.get("API_KEY"), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    necessary_hendlers = [CommandHandler('stop', done),
                          CommandHandler('start', start),
                          CommandHandler('admin', admin)]


    # Payment logic
	dispatcher.add_handler(CommandHandler('pay', pay))
	dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
	dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))


    # Add conversation handler with the states CHOOSE_LANG, ASK_AGE, ASK_AMOUNT, ASK_LOCATION, ASK_PROPS and START_QUERY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ADMIN: [MessageHandler(Filters.text, admin_password),*necessary_hendlers],
            ADMIN_PASSWORD: [MessageHandler(Filters.text, new_password),*necessary_hendlers],
            CHOOSE_LANG: [MessageHandler(Filters.text, set_lang),*necessary_hendlers],
            CHECK_PASSWORD: [MessageHandler(Filters.text, check_password),*necessary_hendlers],
            GAMES: [MessageHandler(Filters.text, game_start),*necessary_hendlers],
            BACK: [MessageHandler(Filters.text, back),*necessary_hendlers],
            ASK_TYPE: [MessageHandler(Filters.text, a_type),*necessary_hendlers],
            ASK_AGE: [MessageHandler(Filters.text, a_age),*necessary_hendlers],
            ASK_AMOUNT: [MessageHandler(Filters.text, a_amount),*necessary_hendlers],
            ASK_LOCATION: [MessageHandler(Filters.text, a_location),*necessary_hendlers],
            ASK_PROPS: [MessageHandler(Filters.text, a_props),*necessary_hendlers],
            RESULT: [MessageHandler(Filters.text, result),*necessary_hendlers],
            ANSWER: [MessageHandler(Filters.text, final_answer),*necessary_hendlers],
            BACK_ANSWER: [MessageHandler(Filters.text, back_answer),*necessary_hendlers],
        },
        fallbacks=[CommandHandler('stop', done)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()