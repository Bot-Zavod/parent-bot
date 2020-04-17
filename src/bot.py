from telegram.ext import Updater, PreCheckoutQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from os import environ

from Logic.Commands import *
from Logic.Payment import *
from Logic.Methods import *
from Logic.Questions import ask_location, ask_type, ask_age, ask_props, result, final_answer, back_answer

from Logic.variables import *

environ["API_KEY"] = '728358108:AAEd0cC2S2LW8HvBSuFbQP0EoA-jWJ5XyUQ'

def main():
    updater = Updater(environ.get("API_KEY"), use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    necessary_hendlers = [CommandHandler('stop', done),
                          CommandHandler('start', start)]
                        # CommandHandler('admin', admin)]

    dispatcher.add_handler(CallbackQueryHandler(subscribe, pattern='^(subscribe)$'))
    dispatcher.add_handler(CallbackQueryHandler(unsubscribe_confirm, pattern='^(unsubscribe_confirm)$'))
    dispatcher.add_handler(CallbackQueryHandler(unsubscribe_done_adm, pattern='^(unsubscribe_done_adm)$'))
    dispatcher.add_handler(CallbackQueryHandler(no_unsubscribe, pattern='^(no_unsubscribe)$'))
    dispatcher.add_handler(CallbackQueryHandler(demo, pattern='^(demo)$'))
    dispatcher.add_handler(CommandHandler('terms', terms))
    dispatcher.add_handler(CommandHandler('subscribe', subscribe))
    dispatcher.add_handler(CommandHandler('unsubscribe', unsubscribe))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_LOCATION: [*necessary_hendlers, MessageHandler(Filters.text, ask_location)],
            ASK_TYPE:     [*necessary_hendlers, MessageHandler(Filters.text, ask_type)],
            ASK_AGE:      [*necessary_hendlers, MessageHandler(Filters.text, ask_age)],
            ASK_PROPS:    [*necessary_hendlers, MessageHandler(Filters.text, ask_props)],
            RESULT:       [*necessary_hendlers, MessageHandler(Filters.text, result)],
            ANSWER:       [*necessary_hendlers, MessageHandler(Filters.text, final_answer)],
            BACK_ANSWER:  [*necessary_hendlers, MessageHandler(Filters.text, back_answer)],

            # PAY: [*necessary_hendlers, MessageHandler(Filters.text, goAndPay)],
            # ADMIN: [MessageHandler(Filters.text, admin_password),*necessary_hendlers],
            BACK: [MessageHandler(Filters.text, back),*necessary_hendlers],
        },
        fallbacks=[CommandHandler('stop', done)]
    )

    dispatcher.add_handler(conv_handler)
    # dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
