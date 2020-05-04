from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from datetime import datetime
from os import getcwd, remove, environ


from .variables import *
from .database import DB
from .etc import text
from .Commands import start
from .spreadsheet import update_games, update_users

push_text_group = None
push_text_notification = None  # for text that admin wants to send


def push_handler(update, context, users_ids):
    global push_text_notification
    for z in users_ids:  # sending the notification message
        context.bot.send_message(chat_id=z, text=push_text_notification)
    user_number = len(users_ids)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text['push_success'].format(user_number=user_number))
    return admin(update, context)


def push_text(update, context):
    global push_text_notification
    push_text_notification = update.message.text
    reply_keyboard = [[text['options_admin']['all'], text['options_admin']['startup']],
                      [text['options_admin']['mentor'], text['options_admin']['partner']]]
    markup = ReplyKeyboardMarkup(
        reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text=text['push_who_q'], reply_markup=markup)
    return PUSH_WHO


def push_who(update, context):
    answer = update.message.text
    if answer == text['options_admin']['all_users']:
        users_ids = DB.get_users()
        return push_handler(update, context, users_ids)
    elif answer == text['options_admin']['payed_users']:
        users_ids = DB.get_users('STARTUP')
        return push_handler(update, context, users_ids)
    elif answer == text['options_admin']['not_payed_users']:
        users_ids = DB.get_users('back')
        return push_handler(update, context, users_ids)
    else:
        return admin(update, context)


def admin_handler(update, context):
    answer = update.message.text
    if answer == text['options_admin']['push']:
        reply_keyboard = [[text['options_admin']['all_users']],
                          [text['options_admin']['payed_users'], text['options_admin']['not_payed_users']],
                          [text["back"]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text(text=text['options_admin']['push_text_q'], reply_markup=markup)
        return PUSH_WHO
    elif answer == text['options_admin']['db']:
        update_result = update_users()
        update.message.reply_text(text=update_result, disable_web_page_preview=True)
        return admin(update, context)
    elif answer == text['options_admin']['update_games']:
        update_result = update_games()
        update.message.reply_text(text=update_result)
        return admin(update, context)
    elif answer == text['back']:
        return start(update, context)
    else:
        return admin(update, context)


# show up basic admin menu
def admin(update, context):
    # checks if you are a true admin
    if update.message.chat.username in environ["ADMIN"]:
        reply_keyboard = [[text['options_admin']['push'], text['options_admin']['db']],
                          [text['options_admin']["update_games"]],
                          [text["back"]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text(
            text=text['options_admin']['hi_boss'], reply_markup=markup)
        return ADMIN
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=text['options_admin']['not_boss'])
        return start(update, context)
