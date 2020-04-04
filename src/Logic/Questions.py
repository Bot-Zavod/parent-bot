from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from variables import *


def a_type(update,context):
    UM.create_user(User(update.message.chat.id,update.message.chat.username))

    UM.currentUsers[update.message.chat.id].set_flag(1)
    reply_keyboard = [[text["team_building"]],[text["ice_breaker"]],[text["timefiller"]],
                      [text["any"],text["back"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_type"], reply_markup = markup)
    return ASK_AGE

def a_age(update,context):
    massage = update.message.text
    if massage == text["team_building"]:
        UM.currentUsers[update.message.chat.id].take_answer(0,0)
    elif massage == text["ice_breaker"]:
        UM.currentUsers[update.message.chat.id].take_answer(0,1)
    elif massage == text["timefiller"]:
        UM.currentUsers[update.message.chat.id].take_answer(0,2)
    elif massage == text["back"] and UM.currentUsers[update.message.chat.id].flag == 1:
        return start_query(update,context)
    elif massage == text["any"]:
        pass
    UM.currentUsers[update.message.chat.id].set_flag(2)

    reply_keyboard = [[text["6-12"],text["12+"]],
                      [text["any"],text["back"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_age"], reply_markup = markup)
    return ASK_AMOUNT

def a_amount(update,context):
    massage = update.message.text
    if massage == text["6-12"]:
        UM.currentUsers[update.message.chat.id].take_answer(1,0)
    elif massage == text["12+"]:
        UM.currentUsers[update.message.chat.id].take_answer(1,1)
    elif massage == text["back"] and UM.currentUsers[update.message.chat.id].flag == 2:
        return a_type(update,context)
    elif massage == text["any"]:
        pass
    UM.currentUsers[update.message.chat.id].set_flag(3)

    reply_keyboard = [[text["up to 5"],text["5-20"],text["20+"]],
                      [text["any"],text["back"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_amount"], reply_markup = markup)
    return ASK_LOCATION

def a_location(update,context):
    massage = update.message.text
    if massage == text["up to 5"]:
        UM.currentUsers[update.message.chat.id].take_answer(2,0)
    elif massage == text["5-20"]:
        UM.currentUsers[update.message.chat.id].take_answer(2,1)
    elif massage == text["20+"]:
        UM.currentUsers[update.message.chat.id].take_answer(2,2)
    elif massage == text["back"] and UM.currentUsers[update.message.chat.id].flag == 3:
        return a_age(update,context)
    elif massage == text["any"]:
        pass
    UM.currentUsers[update.message.chat.id].set_flag(4)

    reply_keyboard = [[text["outside"],text["inside"]],
                      [text["any"],text["back"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_location"], reply_markup = markup)
    return ASK_PROPS

def a_props(update,context):
    massage = update.message.text
    if massage == text["outside"]:
        UM.currentUsers[update.message.chat.id].take_answer(3,0)
    elif massage == text["inside"]:
        UM.currentUsers[update.message.chat.id].take_answer(3,1)
    elif massage == text["back"] and UM.currentUsers[update.message.chat.id].flag == 4:
        return a_amount(update,context)
    elif massage == text["any"]:
        pass
    UM.currentUsers[update.message.chat.id].set_flag(5)

    reply_keyboard = [[text["yes"],text["no"]],
                      [text["any"],text["back"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["ask_props"], reply_markup = markup)
    return RESULT

def result(update,context):
    massage = update.message.text
    if massage == text["no"]:
        UM.currentUsers[update.message.chat.id].take_answer(4,0)
    elif massage == text["yes"]:
        UM.currentUsers[update.message.chat.id].take_answer(4,1)
    elif massage == text["back"] and UM.currentUsers[update.message.chat.id].flag == 5:
        return a_location(update,context)
    elif massage == text["any"]:
        pass
    UM.currentUsers[update.message.chat.id].set_flag(6)

    game_id = get_games_id(update,context)
    update.message.reply_text(game_id)
    buttons_language = "en" if lang == 1 else "ru"
    reply_keyboard = [[names[i][buttons_language]] for i in game_id]
    reply_keyboard.append([text["back"],text["menu"]])
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text["answer"], reply_markup = markup)
    return ANSWER

def final_answer(update,context):
    massage = update.message.text
    if massage == text["back"] and UM.currentUsers[update.message.chat.id].flag == 6:
        return a_props(update,context)
    elif massage == text["menu"]:
        UM.delete_user(update.message.chat.id)
        return start_query(update, context)
    UM.currentUsers[update.message.chat.id].set_flag(7)

    solution = None
    for key in names:
        if massage == names[key]:
            solution = key
            break
    reply_keyboard = [[text["back"],text["menu"]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(games[solution], reply_markup = markup)
    return BACK_ANSWER