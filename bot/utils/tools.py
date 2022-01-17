from typing import Tuple

from telegram import ReplyKeyboardMarkup
from telegram import Update


def send_message_with_keyboard(msg: str, keyboard: list, update: Update):
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(text=msg, reply_markup=markup)


def get_id_msg(update: Update) -> Tuple[int, str]:
    chat_id = update.message.chat.id
    massage = update.message.text
    return chat_id, massage
