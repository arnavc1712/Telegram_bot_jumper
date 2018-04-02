
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from handler import start,help,bookTable,error
from google.appengine.ext import ndb
from model import Tables
import logging
TOKEN = '596189844:AAE4r6eUpOl_dNxb-nAWRASTAl9QRfZCt0o'

bot = telegram.Bot(TOKEN)

dispatcher = None
def setup():
    '''GAE DISPATCHER SETUP'''
    initialize_db()
    global dispatcher
    # Note that update_queue is setted to None and
    # 0 workers are allowed on Google app Engine (If not-->Problems with multithreading)
    dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)

    # ---Register handlers here---
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(MessageHandler(Filters.text, bookTable))
    dispatcher.add_error_handler(error)

    return dispatcher

def webhook(update):
    global dispatcher
    # Manually get updates and pass to dispatcher
    dispatcher.process_update(update)



def initialize_db():
    for i in range(1,19):
        logging.info("Making table {}".format(str(i)))
        tables = Tables()
        
        tables.table_no = i
        tables.booked = False
        tables.key = ndb.Key('Tables', i)
        if i>=7 and i<=12:
            tables.max_occupancy = 4
        elif i>=13 and i<=18:
            tables.max_occupancy = 8
        else:
            tables.max_occupancy = 2
        tables.put()

        
