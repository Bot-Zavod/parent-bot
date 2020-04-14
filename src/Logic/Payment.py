from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from random import randint
from os import environ
import logging
import base64
import json
import hashlib

from .variables import *
from .etc import text

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def subscribe(update, context):
	update = update.callback_query if update.callback_query else update
	public_key = "publick_key"
	private_key = "private_key"
	subscribe_date_start = str(datetime.now().date())+" 00:00:00"
	description = "Subscribe:"+str(update.message.chat.id)+":"+str(update.message.message_id+1)
	result_url = "www.domen.com"
	server_url = "www.domen.com"

	params = {"public_key":public_key,
			  "version":"3",
			  "action":"pay",
			  "amount":"0.3",
			  "currency":"UAH",
			  "description":description,
			  "subscribe_date_start":subscribe_date_start,
			  "subscribe_periodicity":"month",
			  "result_url":result_url,
			  "server_url":result_url,
			  "order_id":randint(0,999999)}

	data = make_data(params)
	signature = make_signature(private_key, data, private_key)

	URL = f"https://www.liqpay.ua/api/3/checkout?data={data}&signature={signature}"
	inline_button = InlineKeyboardButton("Подписаться ✅", url=URL)
	reply_markup = InlineKeyboardMarkup([[inline_button]])
	text = "Прочтите /terms и перейдите по сгенерированной ссылке, для оформления подписки!"
	context.bot.edit_message_text(
		chat_id = update.message.chat.id, 
		message_id = update.message.message_id, 
		text=text, 
		reply_markup=reply_markup
		)
	logger.info("User %s: genetare link to subscribe - %s;", update.message.chat.id, URL)

def make_data(params):
	json_data = json.dumps(params).encode('utf-8')
	data = base64.b64encode(json_data).decode('utf-8')
	return data

def make_signature(*args):
	joined_fields = ''.join(x  for x in args)
	sha = hashlib.sha1(joined_fields.encode('utf-8')).digest()
	res = base64.b64encode(sha).decode('utf-8')
	return res