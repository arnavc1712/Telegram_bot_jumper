import telegram
from flask import Flask, request,session
import logging
import copy
from Queue import Queue
from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from credentials import TOKEN
from setup import setup,webhook
from handler import start,help,bookTable, error
from model import Account, Tables


app = Flask(__name__)

app.secret_key = 'some_secret'

dispatcher = None
bot = telegram.Bot(TOKEN)


@app.route('/HOOK', methods=['POST'])
def webhook_handler():
	if request.method == "POST":
    	
        # retrieve the message in JSON and then transform it to Telegram object
      
		update = telegram.Update.de_json(request.get_json(force=True), bot)
		if update:
			webhook(update)

	return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
	setup()
	s = bot.setWebhook('https://telegram-bot-rest.appspot.com/HOOK')
	# s = bot.setWebhook('https://telegram-bot-rest.appspot.com/HOOK')
	if s:
	    return "webhook setup ok"
	else:
	    return "webhook setup failed"


@app.route('/')
def index():
    return '.'





if __name__ == "__main__":
    app.run(debug=True)