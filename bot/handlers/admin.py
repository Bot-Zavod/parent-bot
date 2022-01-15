import os

from telegram import ReplyKeyboardMarkup

from bot.handlers.base import start
from bot.data import text
from bot.database import db_interface
from bot.utils.spreadsheet import update_games
from bot.states import State

push_text_group = None
push_text_notification = None  # for text that admin wants to send


def update_users():
    pass


def push_handler(update, context):
    msg = update.message.text
    if msg != text["options_admin"]["send"]:
        return admin(update, context)

    global push_text_notification
    global push_text_group
    # sending the notification message
    users_ids = db_interface.get_users(push_text_group)
    for z in users_ids:
        context.bot.send_message(chat_id=z, text=push_text_notification)
    user_number = len(users_ids)
    update.message.reply_text(
        text=text["options_admin"]["push_success"].format(user_number=user_number)
    )
    return admin(update, context)


def push_text(update, context):
    """catches admin massage"""
    global push_text_notification
    answer = update.message.text
    push_text_notification = answer

    reply_keyboard = [[text["options_admin"]["send"], text["options_admin"]["no_send"]]]
    markup = ReplyKeyboardMarkup(
        reply_keyboard, resize_keyboard=True, one_time_keyboard=True
    )
    msg = text["options_admin"]["push_submit"].format(answer=answer)
    update.message.reply_text(text=msg, reply_markup=markup)
    return State.PUSH_SUBMIT


def push_who(update, context):
    """push menu"""
    global push_text_group
    answer = update.message.text

    def push_text_direct(update, context):
        update.message.reply_text(text=text["options_admin"]["push_text"])
        return State.PUSH_WHAT

    if answer == text["options_admin"]["all_users"]:
        return push_text_direct(update, context)
    elif answer == text["options_admin"]["payed_users"]:
        push_text_group = "PAYED"
        return push_text_direct(update, context)
    elif answer == text["options_admin"]["not_payed_users"]:
        push_text_group = "UNPAYED"
        return push_text_direct(update, context)
    else:
        return admin(update, context)


def admin_handler(update, context):
    """handle answer from admin menu"""
    answer = update.message.text
    if answer == text["options_admin"]["push"]:
        reply_keyboard = [
            [text["options_admin"]["all_users"]],
            [
                text["options_admin"]["payed_users"],
                text["options_admin"]["not_payed_users"],
            ],
            [text["back"]],
        ]
        markup = ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=True
        )
        update.message.reply_text(
            text=text["options_admin"]["push_text_q"], reply_markup=markup
        )
        return State.PUSH_WHO
    elif answer == text["options_admin"]["db"]:
        update_result = update_users()
        update.message.reply_text(text=update_result, disable_web_page_preview=True)
        return admin(update, context)
    elif answer == text["options_admin"]["update_games"]:
        update_result = update_games()
        update.message.reply_text(text=update_result)
        return admin(update, context)
    elif answer == text["options_admin"]["users"]:
        users_count = db_interface.users_count()
        msg = (
            f"Воспользовались: {users_count[0]}\n"
            + f"Подписались: {users_count[1]}\n"
            + f"Отписались: {users_count[2]}"
        )
        update.message.reply_text(text=msg)
        return admin(update, context)
    elif answer == text["back"]:
        return start(update, context)
    else:
        return admin(update, context)


def admin_menu(update, context):
    """show up basic admin menu"""
    # checks if you are a true admin
    if update.message.chat.username in os.getenv("ADMIN"):
        reply_keyboard = [
            [text["options_admin"]["push"], text["options_admin"]["users"]],
            [text["options_admin"]["db"], text["options_admin"]["update_games"]],
            [text["back"]],
        ]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text(
            text=text["options_admin"]["hi_boss"], reply_markup=markup
        )
        return State.ADMIN
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=text["options_admin"]["not_boss"]
        )
        return start(update, context)
