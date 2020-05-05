from telegram.ext import Updater, PreCheckoutQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from os import environ, path

from Logic.Commands import *
from Logic.Payment import *
from Logic.Methods import *
from Logic.Questions import ask_location, ask_type, ask_age, ask_props, result, final_answer, back_answer
from Logic.variables import *
from Logic.Admin import *

def env():
    enviroment = ".env"
    create_path = path.abspath(getcwd())
    create_path = path.join(create_path, "src", enviroment)

    if not path.exists(create_path):
        print("no .env found")
        print(f"create_path: {create_path}")
        f = open(create_path, "x")
        f.close()
        print(".env need to be completed")
    else:
        print(".env exist")
env()

from dotenv import load_dotenv
load_dotenv()

print("Modules import succesfull")


def main():

    token = environ["API_KEY"]
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    necessary_hendlers = [CommandHandler('stop', done),
                          CommandHandler('start', start),
                          CommandHandler('admin', admin)]

    dispatcher.add_handler(CallbackQueryHandler(
        subscribe, pattern='^(subscribe)$'))
    dispatcher.add_handler(CallbackQueryHandler(
        unsubscribe_confirm, pattern='^(unsubscribe_confirm)$'))
    dispatcher.add_handler(CallbackQueryHandler(
        subprocessing, pattern='^(month|year)$'))
    dispatcher.add_handler(CallbackQueryHandler(
        no_unsubscribe, pattern='^(no_unsubscribe)$'))
    dispatcher.add_handler(CallbackQueryHandler(demo, pattern='^(demo)$'))
    dispatcher.add_handler(CommandHandler('info', terms))
    dispatcher.add_handler(CommandHandler('subscribe', subscribe))
    dispatcher.add_handler(CommandHandler('unsubscribe', unsubscribe))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      CommandHandler('admin', admin)],
        states={
            ASK_LOCATION: [*necessary_hendlers, MessageHandler(Filters.text, ask_location)],
            ASK_TYPE:     [*necessary_hendlers, MessageHandler(Filters.text, ask_type)],
            ASK_AGE:      [*necessary_hendlers, MessageHandler(Filters.text, ask_age)],
            ASK_PROPS:    [*necessary_hendlers, MessageHandler(Filters.text, ask_props)],
            RESULT:       [*necessary_hendlers, MessageHandler(Filters.text, result)],
            ANSWER:       [*necessary_hendlers, MessageHandler(Filters.text, final_answer)],
            BACK_ANSWER:  [*necessary_hendlers, MessageHandler(Filters.text, back_answer)],

            ADMIN:        [*necessary_hendlers, MessageHandler(Filters.text, admin_handler)],
            PUSH_WHO:     [*necessary_hendlers, MessageHandler(Filters.text, push_who)],
            PUSH_WHAT:    [*necessary_hendlers, MessageHandler(Filters.text, push_text)],
            PUSH_SUBMIT:  [*necessary_hendlers, MessageHandler(Filters.text, push_handler)],
            

        },
        fallbacks=[CommandHandler('stop', done)]
    )

    dispatcher.add_handler(conv_handler)
    # dispatcher.add_error_handler(error)
    updater.start_polling()
    print("Bot launched succesfully")
    updater.idle()


if __name__ == '__main__':
    main()
