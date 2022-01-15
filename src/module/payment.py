from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from random import randint
from os import environ
import logging
import base64
import json
import hashlib
from .Commands import start
from .variables import *
from .etc import text
from .database import DB
from urllib.parse import urlencode
from urllib.request import urlopen
import contextlib
from requests import post

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def subscribe(update, context):
    update = update.callback_query if update.callback_query else update
    chat_id = update.message.chat.id

    # Here must be checking status of payment for user. Is it subscribed -> True=> sendMessage('You already have a subscription')
    # status = unsubscribed or absent -> continue
    isPayed = DB.is_subscribed(chat_id)
    if isPayed:
        update.message.reply_text(text["already_subscribed"])
        return start(update, context)
    month = InlineKeyboardButton(text='Месяц', callback_data="month")
    year = InlineKeyboardButton(text='Год', callback_data="year") 
    reply_markup = InlineKeyboardMarkup([[month], [year]])
    context.bot.send_message(
        chat_id=update.message.chat.id,
        text="Выберите срок подписки",
        reply_markup=reply_markup
    )
    logger.info("User %s: ask to subscribe", update.message.chat.id)

def subprocessing(update, context):
    update = update.callback_query if update.callback_query else update
    chat_id = update.message.chat.id
    term = update.data

    public_key = environ["PUBLIC_KEY"]
    private_key = environ["PRIVAT_KEY"]
    subscribe_date_start = str(datetime.now().date())+" 00:00:00"
    description = "Subscribe:" + \
        str(update.message.chat.id)+":"+str(update.message.message_id+1)
    result_url = "https://t.me/superparent_bot"
    server_url = environ["SERVER"]

    params = {"public_key": public_key,
              "version": "3",
              "action": "subscribe",
              "amount": "0.3",
              "currency": "UAH",
              "description": description,
              "subscribe_date_start": subscribe_date_start,
              "subscribe_periodicity": term,
              "result_url": result_url,
              "server_url": server_url,
              "order_id": randint(0, 999999)}

    data = make_data(params)
    signature = make_signature(private_key, data, private_key)

    URL = make_tiny(
        f"https://www.liqpay.ua/api/3/checkout?data={data}&signature={signature}")
    inline_button = InlineKeyboardButton(text["pay"], url=URL)
    reply_markup = InlineKeyboardMarkup([[inline_button]])
    context.bot.delete_message(
        chat_id=update.message.chat.id,
        message_id=update.message.message_id,
    )
    context.bot.send_message(
        chat_id=update.message.chat.id,
        # message_id=update.message.message_id,
        text=text["pay_intro"],
        reply_markup=reply_markup
    )
    logger.info("User %s: (term: %s)genetare link to subscribe - %s;",
                update.message.chat.id, term, URL)


def unsubscribe(update, context):
    chat_id = update.message.chat.id
    isPayed = DB.is_subscribed(chat_id)
    if not isPayed:
        update.message.reply_text(text=text["not_subscribed"])
        return start(update, context)
    button1 = InlineKeyboardButton(
        text["unsubscribe"], callback_data="unsubscribe_confirm")
    button2 = InlineKeyboardButton(
        text["do_not_unsubscribe"], callback_data="no_unsubscribe")
    reply_markup = InlineKeyboardMarkup([[button1], [button2]])
    update.message.reply_text(
        text=text["ask_to_unsubscribe"], reply_markup=reply_markup)
    logger.info("User %s: ask Unsubscribe;", update.message.chat.id)


def unsubscribe_confirm(update, context):
    chat_id = update.callback_query.message.chat.id
    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=update.callback_query.message.message_id,
        text=text["unsubscribe_sent"],
    )
    logger.info("User %s: confirm Unsubscribe;", chat_id)
    return unsubscribe_request(update, context)


#post request Server-Server to Unsubscribe
def unsubscribe_request(update, context):
    update = update.callback_query if update.callback_query else update
    chat_id = update.message.chat.id
    order_id = DB.get_order_id(chat_id)
    public_key = environ["PUBLIC_KEY"]
    private_key = environ["PRIVAT_KEY"]
    params = {
      "public_key": public_key,
      "action":"unsubscribe",
      "version":"3",
      "order_id":order_id}
    data = make_data(params)
    signature = make_signature(private_key, data, private_key)
    url = "https://www.liqpay.ua/api/request"
    res = post(url, {'data':data, 'signature':signature}).json()
    print(res)
    logger.info("User %s: %s", chat_id, res)
    if res['result'] == 'ok':
	#HERE must be method that change status on unsubscribe
        status_res = DB.set_status('unsubscribe', chat_id)
        context.bot.edit_message_text(chat_id=chat_id, message_id=update.message.message_id, text=text["done"])
    else:
        logger.info(f"User {chat_id}: unsubscribe with status = {res['result']}")


#def unsubscribe_done_adm(update, context):
#    payment_id = int(update.callback_query.message.text.split()[1])
#    print(f"payment_id unsubscribed: {payment_id}")
#    # mark paymetn_id as unsubscribed
#    DB.unsubscribe_user(payment_id)
#    context.bot.edit_message_text(
#        chat_id=update.callback_query.message.chat.id,
#        message_id=update.callback_query.message.message_id,
#        text=text["unsubscribe_processed"],
#    )
#    logger.info("Admin: process app;")


def no_unsubscribe(update, context):
    context.bot.delete_message(
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
    )
    return start(update.callback_query, context)


def make_data(params):
    json_data = json.dumps(params).encode('utf-8')
    data = base64.b64encode(json_data).decode('utf-8')
    return data


def make_signature(*args):
    joined_fields = ''.join(x for x in args)
    sha = hashlib.sha1(joined_fields.encode('utf-8')).digest()
    res = base64.b64encode(sha).decode('utf-8')
    return res


def make_tiny(url):
    request_url = ('http://tinyurl.com/api-create.php?' +
                   urlencode({'url': url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8 ')
