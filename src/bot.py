from telegram.ext import (Updater, PreCheckoutQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from os import environ

from Logic.Commands import *
from Logic.Payment import *
from Logic.Methods import *
from variables import *


def main():
    updater = Updater(environ.get("API_KEY"), use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    necessary_hendlers = [CommandHandler('stop', done),
                          CommandHandler('start', start),
                          CommandHandler('terms', terms)]
                        # CommandHandler('admin', admin)]

    # Payment logic
    dispatcher.add_handler(CommandHandler('pay', pay))
    dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))

    # Add conversation handler with the states CHOOSE_LANG, ASK_AGE, ASK_AMOUNT, ASK_LOCATION, ASK_PROPS and START_QUERY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PAY: [*necessary_hendlers, MessageHandler(Filters.text, goAndPay)],
            # ADMIN: [MessageHandler(Filters.text, admin_password),*necessary_hendlers],
            GAMES: [MessageHandler(Filters.text, game_start),*necessary_hendlers],
            BACK: [MessageHandler(Filters.text, back),*necessary_hendlers],
            # ASK_TYPE: [MessageHandler(Filters.text, a_type),*necessary_hendlers],
            # ASK_AGE: [MessageHandler(Filters.text, a_age),*necessary_hendlers],
            # ASK_AMOUNT: [MessageHandler(Filters.text, a_amount),*necessary_hendlers],
            # ASK_LOCATION: [MessageHandler(Filters.text, a_location),*necessary_hendlers],
            # ASK_PROPS: [MessageHandler(Filters.text, a_props),*necessary_hendlers],
            # RESULT: [MessageHandler(Filters.text, result),*necessary_hendlers],
            # ANSWER: [MessageHandler(Filters.text, final_answer),*necessary_hendlers],
            BACK_ANSWER: [MessageHandler(Filters.text, back_answer),*necessary_hendlers],
        },
        fallbacks=[CommandHandler('stop', done)]
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
