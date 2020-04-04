from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from Logic.Payment import pay, successful_payment_callback, precheckout_callback
from etc import text
from os import getcwd, environ
from random import randint
from database import DbInterface
from user import UserManager, User

CHOOSE_LANG, CHECK_PASSWORD, ADMIN, GAMES, BACK, ASK_TYPE,\
ASK_AGE, ASK_AMOUNT, ASK_LOCATION, ASK_PROPS, RESULT,\
ANSWER,BACK_ANSWER, ADMIN_PASSWORD = range(14)

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