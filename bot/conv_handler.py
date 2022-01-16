from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

from bot.data import text
from bot.handlers.admin import admin_menu
from bot.handlers.admin import ask_push_text
from bot.handlers.admin import list_users
from bot.handlers.admin import push_handler
from bot.handlers.admin import set_push_text
from bot.handlers.admin import update_games_tables
from bot.handlers.base import start
from bot.handlers.base import stop_bot
from bot.handlers.questions import ask_age
from bot.handlers.questions import ask_location
from bot.handlers.questions import ask_props
from bot.handlers.questions import ask_type
from bot.handlers.questions import back_answer
from bot.handlers.questions import final_answer
from bot.handlers.questions import result
from bot.states import State
from bot.utils.methods import *


must_commands = [
    CommandHandler("start", start),
    CommandHandler("stop", stop_bot),
    CommandHandler("admin", admin_menu),
]

states = {
    State.ASK_LOCATION: [MessageHandler(Filters.text, ask_location)],
    State.ASK_TYPE: [MessageHandler(Filters.text, ask_type)],
    State.ASK_AGE: [MessageHandler(Filters.text, ask_age)],
    State.ASK_PROPS: [MessageHandler(Filters.text, ask_props)],
    State.RESULT: [MessageHandler(Filters.text, result)],
    State.ANSWER: [MessageHandler(Filters.text, final_answer)],
    State.BACK_ANSWER: [MessageHandler(Filters.text, back_answer)],
    State.ADMIN: [
        MessageHandler(Filters.text([text["options_admin"]["push"]]), ask_push_text),
        MessageHandler(
            Filters.text([text["options_admin"]["update_games"]]), update_games_tables
        ),
        MessageHandler(Filters.text([text["options_admin"]["users"]]), list_users),
        MessageHandler(Filters.text([text["back"]]), start),
    ],
    State.PUSH_WHAT: [MessageHandler(Filters.text, set_push_text)],
    State.PUSH_SUBMIT: [
        MessageHandler(
            Filters.text(
                [text["options_admin"]["send"], text["options_admin"]["no_send"]]
            ),
            push_handler,
        )
    ],
}

for key, value in states.items():
    states[key] = must_commands + value

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start), CommandHandler("admin", admin_menu)],
    states=states,
    fallbacks=[CommandHandler("stop", stop_bot)],
)
