from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PreCheckoutQueryHandler
from telegram import LabeledPrice
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)



def start(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Привет дорогой друг! Чтобы купить кожуру банана, напиши /pay 🍌")
	logger.info("User %s: send /start command", update.message.chat.id)

def pay(update, context):
	context.bot.send_invoice(chat_id=update.effective_chat.id, 
							 title="Процесс покупки",
							 description="Кожура сомалийского банана 🍌",
							 payload="banana-peel",
							 start_parameter="banana-peel-test",
							 provider_token="635983722:LIVE:i39987050522",
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
	# Вот тут мы заносим пользователя в базу, что он купил
	update.message.reply_text("Дело сделано! Кожура в пути!")

def precheckout_callback(update, context):
    query = update.pre_checkout_query
    if query.invoice_payload != 'banana-peel':
        query.answer(ok=False, error_message="Говно получилось какое-то...")
    else:    	
        query.answer(ok=True)





if __name__ == '__main__':
	updater = Updater(token='728358108:AAEd0cC2S2LW8HvBSuFbQP0EoA-jWJ5XyUQ', use_context=True)
	dispatcher = updater.dispatcher

	start_handler = CommandHandler('start', start)
	dispatcher.add_handler(start_handler)

	pay_handler = CommandHandler('pay', pay)
	dispatcher.add_handler(pay_handler)

	payment_check = PreCheckoutQueryHandler(precheckout_callback)
	dispatcher.add_handler(payment_check)

	payment = MessageHandler(Filters.successful_payment, successful_payment_callback)
	dispatcher.add_handler(payment)

	updater.start_polling()
	updater.idle()