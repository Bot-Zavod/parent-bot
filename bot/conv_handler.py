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
from bot.handlers.games import ask_age
from bot.handlers.games import ask_games
from bot.handlers.games import ask_location
from bot.handlers.games import ask_props
from bot.handlers.games import ask_type
from bot.handlers.games import get_age
from bot.handlers.games import get_games
from bot.handlers.games import get_location
from bot.handlers.games import get_props
from bot.handlers.games import get_random_game
from bot.handlers.games import get_type
from bot.states import State


must_commands = [
    CommandHandler("start", start),
    CommandHandler("stop", stop_bot),
    CommandHandler("admin", admin_menu),
]

states = {
    State.MENU: [
        MessageHandler(Filters.text([text["games"]]), ask_location),
        MessageHandler(Filters.text([text["random"]]), get_random_game),
    ],
    State.GET_LOCATION: [
        MessageHandler(Filters.text([text["inside"], text["outside"]]), get_location),
        MessageHandler(Filters.text([text["trip"]]), ask_age),  # skip type
        MessageHandler(Filters.text([text["back"]]), start),
    ],
    State.GET_TYPE: [
        MessageHandler(
            Filters.text(
                [
                    text["active"],
                    text["educational"],
                    text["calming"],
                    text["family"],
                    text["task"],
                ]
            ),
            get_type,
        ),
        MessageHandler(Filters.text([text["back"]]), ask_location),
    ],
    State.GET_AGE: [
        MessageHandler(
            Filters.text([text["2-3"], text["3-4"], text["4-6"], text["6-8"]]), get_age
        ),
        MessageHandler(Filters.text([text["back"]]), ask_type),
    ],
    State.GET_PROPS: [
        MessageHandler(Filters.text([text["yes"], text["no"]]), get_props),
        MessageHandler(Filters.text([text["back"]]), ask_age),
    ],
    State.GET_GAME: [
        MessageHandler(Filters.text([text["back"]]), ask_props),
        MessageHandler(Filters.text([text["menu"]]), start),
        MessageHandler(Filters.text, get_games),
    ],
    State.BACK_ANSWER: [
        MessageHandler(Filters.text([text["back"]]), ask_games),
        MessageHandler(Filters.text([text["menu"]]), start),
    ],
    # =======================================================
    # ADMIN
    # =======================================================
    State.ADMIN: [
        MessageHandler(Filters.text([text["push"]]), ask_push_text),
        MessageHandler(Filters.text([text["update_games"]]), update_games_tables),
        MessageHandler(Filters.text([text["users"]]), list_users),
        MessageHandler(Filters.text([text["back"]]), start),
    ],
    State.PUSH_WHAT: [MessageHandler(Filters.text, set_push_text)],
    State.PUSH_SUBMIT: [
        MessageHandler(Filters.text([text["cancel"]]), admin_menu),
        MessageHandler(Filters.text([text["send"]]), push_handler),
    ],
}

for key, value in states.items():
    states[key] = must_commands + value

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start), CommandHandler("admin", admin_menu)],
    states=states,
    fallbacks=[CommandHandler("stop", stop_bot)],
)
