
import telegram
from google.appengine.ext import ndb
from model import Account, Tables
import logging
# from logging import logger

TOKEN = '596189844:AAE4r6eUpOl_dNxb-nAWRASTAl9QRfZCt0o'
bot = telegram.Bot(TOKEN)


def start(bot, update):

	ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
	chat_id = update.message.chat_id
	user_id = update.message.from_user.id
	user_obj = bot.getChat(chat_id)
	ancestor_key = ndb.Key('Account',user_id or '*notitle*')
	curr_user = Account.query_users(ancestor_key).fetch()

	if not curr_user:
		account = create_entity_using_keyword_arguments(user_obj,user_id)
		account.key = ndb.Key('Account', user_id)
		account.put()
		# ancestor_key = ndb.Key('Account',user_id or '*notitle*')
		curr_user = Account.query_users(account.key).fetch()
		bot.sendMessage(chat_id = chat_id,text = "Welcome to the Booking Bot, {}.\n How many people?".format(user_obj["first_name"]))
	else:
		user = ancestor_key.get()
		user.entries += 1
		user.put()
		bot.sendMessage(chat_id = chat_id,text="""Welcome again to the Booking Bot {}.\nThis is your {} time here.
			\nHow many people?""".format(user_obj["first_name"],ordinal(user.entries)))

    # bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def bookTable(bot, update):
	no_people = int(update.message.text)
	# query_tables = Tables.query().filter(Tables.max_occupancy >= no_people,Tables.booked == False)
	# logging.info("enter no people is {}".format(no_people))
	query_tables = Tables.query().filter(Tables.max_occupancy >= no_people).filter(Tables.booked == False)
	for i in query_tables.fetch():
		logging.info("Query tables are {} {}".format(dict(i)["booked"],dict(i)["max_occupancy"]))
	bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logging.info('Update {} caused error {}'.format(update, error))



def create_entity_using_keyword_arguments(user_dict,userid,entries = 1):
    user = Account()
    # logging.info("USer obj looks like {}".format(dict(user_dict)))
    
    # user_dict = {unicode(k).encode("utf-8"): unicode(v).encode("utf-8") for k,v in dict(user_dict).iteritems()}
    if user_dict["last_name"]:
        user.username = user_dict["first_name"] + " " + user_dict["last_name"]
    else:
        user.username = user_dict["first_name"]
    user.userid=userid
    user.entries = entries
    # user.phone_no = user_dict["phone_number"]
    return user