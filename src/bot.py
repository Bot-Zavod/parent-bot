from os import environ
from os import path

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import PreCheckoutQueryHandler
from telegram.ext import Updater

from src.admin import *
from src.commands import *
from src.methods import *
from src.payment import *
from src.questions import ask_age
from src.questions import ask_location
from src.questions import ask_props
from src.questions import ask_type
from src.questions import back_answer
from src.questions import final_answer
from src.questions import result
from src.states import State


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

load_dotenv()

print("srcs import succesfull")


def main():

    token = environ["API_KEY"]
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    necessary_hendlers = [
        CommandHandler("stop", done),
        CommandHandler("start", start),
        CommandHandler("admin", admin),
    ]

    dispatcher.add_handler(CallbackQueryHandler(subscribe, pattern="^(subscribe)$"))
    dispatcher.add_handler(
        CallbackQueryHandler(unsubscribe_confirm, pattern="^(unsubscribe_confirm)$")
    )
    dispatcher.add_handler(
        CallbackQueryHandler(subprocessing, pattern="^(month|year)$")
    )
    dispatcher.add_handler(
        CallbackQueryHandler(no_unsubscribe, pattern="^(no_unsubscribe)$")
    )
    dispatcher.add_handler(CallbackQueryHandler(demo, pattern="^(demo)$"))
    dispatcher.add_handler(CommandHandler("info", terms))
    dispatcher.add_handler(CommandHandler("subscribe", subscribe))
    dispatcher.add_handler(CommandHandler("unsubscribe", unsubscribe))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler("admin", admin)],
        states={
            State.ASK_LOCATION: [
                *necessary_hendlers,
                MessageHandler(Filters.text, ask_location),
            ],
            State.ASK_TYPE: [
                *necessary_hendlers,
                MessageHandler(Filters.text, ask_type),
            ],
            State.ASK_AGE: [*necessary_hendlers, MessageHandler(Filters.text, ask_age)],
            State.ASK_PROPS: [
                *necessary_hendlers,
                MessageHandler(Filters.text, ask_props),
            ],
            State.RESULT: [*necessary_hendlers, MessageHandler(Filters.text, result)],
            State.ANSWER: [
                *necessary_hendlers,
                MessageHandler(Filters.text, final_answer),
            ],
            State.BACK_ANSWER: [
                *necessary_hendlers,
                MessageHandler(Filters.text, back_answer),
            ],
            State.ADMIN: [
                *necessary_hendlers,
                MessageHandler(Filters.text, admin_handler),
            ],
            State.PUSH_WHO: [
                *necessary_hendlers,
                MessageHandler(Filters.text, push_who),
            ],
            State.PUSH_WHAT: [
                *necessary_hendlers,
                MessageHandler(Filters.text, push_text),
            ],
            State.PUSH_SUBMIT: [
                *necessary_hendlers,
                MessageHandler(Filters.text, push_handler),
            ],
        },
        fallbacks=[CommandHandler("stop", done)],
    )

    dispatcher.add_handler(conv_handler)
    # dispatcher.add_error_handler(error)
    updater.start_polling()
    print("Bot launched succesfully")
    updater.idle()


if __name__ == "__main__":
    main()
