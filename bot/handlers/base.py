import html
import json
import os
import sys
import traceback

from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler

from bot.data import text
from bot.database import db_interface
from bot.states import State
from bot.user_manager import user_manager
from bot.utils.log import log_message
from bot.utils.tools import send_message_with_keyboard


def start(update: Update, context: CallbackContext):
    log_message(update)

    chat_id = update.message.chat.id
    db_interface.save_id(chat_id)
    user_manager.delete_user(chat_id)

    keyboard = [[text["games"]], [text["random"]]]
    send_message_with_keyboard(text["start_games"], keyboard, update)
    return State.MENU


def stop_bot(update: Update, context: CallbackContext):
    log_message(update)
    update.message.reply_text(text["stop"])
    return ConversationHandler.END


def terms(update: Update, context: CallbackContext):
    log_message(update)
    update.message.reply_text(text["terms"])


def error_handler(update: Update, context: CallbackContext):
    """Log the error and send a telegram message to notify the developer"""
    # we want to notify the user of this problem.
    # This will always work, but not notify users if the update is an
    # callback or inline query, or a poll update.
    # In case you want this, keep in mind that sending the message could fail

    if update:
        local_upd = (
            update.effective_message if update.effective_message else update.message
        )
    else:
        local_upd = None

    chat_id = None
    if local_upd:
        chat_id = local_upd.chat.id
        context.bot.send_message(
            chat_id=chat_id,
            text=text["server_error"],
        )

    # Log the error before we do anything else, so we can see it even if something breaks.

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    error_tb = "".join(tb_list)
    logger.bind(chat_id=chat_id).error(f"Exception while handling an update:{error_tb}")
    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    bot_username = "@" + context.bot.username + "\n\n"
    if update:
        update_json = json.dumps(update.to_dict(), indent=2, ensure_ascii=False)
    else:
        update_json = ""
    error_message = (
        "{}"
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>context.chat_data = {}</pre>\n\n"
        "<pre>context.user_data = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        bot_username,
        html.escape(update_json),
        html.escape(str(context.chat_data)),
        html.escape(str(context.user_data)),
        html.escape(error_tb),
    )

    # Finally, send the message
    log_channel = "@" + os.environ["LOG_CHANNEL"]

    # dont print to debug channel in case that's not a production server
    if ("--debug" not in sys.argv) and ("-d" not in sys.argv):
        if len(error_message) < 4096:
            context.bot.send_message(chat_id=log_channel, text=error_message)
        else:
            msg_parts = len(error_message) // 4080
            for i in range(msg_parts):
                err_msg_truncated = error_message[i : i + 4080]
                if i == 0:
                    error_message_text = err_msg_truncated + "</pre>"
                elif i < msg_parts:
                    error_message_text = "<pre>" + err_msg_truncated + "</pre>"
                else:
                    error_message_text = "<pre>" + err_msg_truncated
                context.bot.send_message(chat_id=log_channel, text=error_message_text)
