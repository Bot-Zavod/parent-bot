from telegram import LabeledPrice, ReplyKeyboardMarkup
from os import environ
import logging

from variables import *
from etc import text

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def terms(update, context):
	update.message.reply_text(text["terms"])

def goAndPay(update, context):
	"""" Tell user that he needs to pay and provide
	keyboard to check out our terms and demo games"""
	massage = update.message.text
	if massage == text["pay_please"]:
		reply_keyboard = [[text["demo"]]]
		markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
		update.message.reply_text(text["pay_intro"], reply_markup = markup)
	else:
		update.message.reply_text(text["unknown"])
		return PAY

def prePay(update, context):
	""" Catch an answer from previous function ^
	shows terms and demo games"""
	massage = update.message.text
	if massage == text["demo"]:
		# reply_keyboard = [[text["demo"]]]
		# markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
		update.message.reply_text("your demo") #, reply_markup = markup)
	else:
		update.message.reply_text(text["unknown"])
		return PAY


def pay(update, context):
	context.bot.send_invoice(chat_id=update.effective_chat.id, 
							 title="Процесс покупки",
							 description="Кожура сомалийского банана 🍌",
							 payload="banana-peel",
							 start_parameter="banana-peel-test",
							 provider_token=environ.get("LiqPay_TOKEN"),
							 photo_url="https://static.turbosquid.com/Preview/2017/03/07__10_55_39/BananaPeel.png0852BE94-70F8-4F85-B598-F98D0AD1137CZoom.jpg",
							 photo_height=512,
							 photo_width=512,
							 photo_size=512,
							 is_flexible=False,
							 currency="UAH", #UAH 980
							 prices=[LabeledPrice("Peel", 50)],							 
							 send_email_to_provider=True							 
							 )
	logger.info("User %s: try to ut bananas peel", update.message.chat.id)



def successful_payment_callback(update, context):
	# It should be noted in the database that the user paid
	update.message.reply_text("Well done! Pell on way!")



def precheckout_callback(update, context):
    query = update.pre_checkout_query
    if query.invoice_payload != 'banana-peel':
        query.answer(ok=False, error_message="Shit happens...")
    else:    	
        query.answer(ok=True)

