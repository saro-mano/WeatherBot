import time
import requests
import json
import pprint
import telegram
import sqlite3
from telegram import InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton,ReplyKeyboardMarkup
from telegram.ext import Updater,CommandHandler,MessageHandler,CallbackQueryHandler,Filters


bot_token = "909999620:AAGA3pzw8ZPAa2lEM1Zp-pTPoqr719xPZiI"

bot=telegram.Bot(token=bot_token)
updater = Updater(token=bot_token,use_context=True)
connection = sqlite3.connect('/Users/saravananmano/Desktop/Weather/weather.db',check_same_thread=False)
print(connection)

def start(update, context):
	bot.send_message(chat_id=update.effective_chat.id, text='Hi, I am a weather bot')

def add(update, context):
	bot.send_message(chat_id=update.effective_chat.id, text='Please enter the city to be added')

def weather(update, context):
	id = update.effective_chat.id
	query = "SELECT * from city where id = {}".format(id)
	cursor = connection.execute(query)
	fetched = cursor.fetchall()
	list_of_cities = list()
	for each in fetched:
		list_of_cities.append(each[1])
	list_of_cities = list(set(list_of_cities)) #remove dups
	button_list = []
	for each in list_of_cities:
		button_list.append(InlineKeyboardButton(each, callback_data = each))
	reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
	bot.send_message(chat_id=update.message.chat_id, text='Choose from the following',reply_markup=reply_markup)

def remove(update, context):
	id = update.effective_chat.id
	query = "SELECT * from city where id = {}".format(id)
	cursor = connection.execute(query)
	fetched = cursor.fetchall()
	list_of_cities = list()
	for each in fetched:
		list_of_cities.append(each[1])
	list_of_cities = list(set(list_of_cities))
	button_list = []
	for each in list_of_cities:
		button_list.append(InlineKeyboardButton(each, callback_data = each + ",remove"))
	reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
	bot.send_message(chat_id=update.message.chat_id, text='Select the one to be removed',reply_markup=reply_markup)

def stop(update, context):
	updater.stop()
	bot.send_message(chat_id = update.effective_chat.id, text='See you soon!')

def database(id,city):
	connection.execute("INSERT INTO city VALUES(?,?)",(id,city))
	connection.commit()
	print(city,'added successfully to the DB!')
	bot.send_message(chat_id=id, text='Added successfully!')

def callback(update, context):
	callbackquery = update.callback_query
	city = callbackquery.data
	if ("remove" not in city):
		try:
			api_address='http://api.openweathermap.org/data/2.5/weather?appid=fe77c384145449cdd1bbf0dc8b027998&q='
			url = api_address + str(city)
			json_data = requests.get(url).json()
			pp = pprint.PrettyPrinter(indent=4) #reference
			temp_in_kelvin = json_data['main']['temp']
			temp_in_cel = int(temp_in_kelvin)-273.15
			bot.send_message(chat_id=update.effective_chat.id, text='The current temperature in {} is {}°C'.format(city,round(temp_in_cel)))
			print("Found!")
		except:
			bot.send_message(chat_id=update.effective_chat.id, text='The entered city name is invalid')
	else:
		removequery(update.effective_chat.id,city)

def findweather(update, context):
	city = update.message.text
	id = update.effective_chat.id
	if valid(city):
		database(id,city)
	else:
		bot.send_message(chat_id=id, text='Please enter a valid city!')

def valid(city):
	try:
		api_address='http://api.openweathermap.org/data/2.5/weather?appid=fe77c384145449cdd1bbf0dc8b027998&q='
		url = api_address + str(city)
		json_data = requests.get(url).json()
		pp = pprint.PrettyPrinter(indent=4) #reference
		temp_in_kelvin = json_data['main']['temp']
		return True
	except:
		return False

def removequery(id,city):
	city = city.split(",")[0]
	query = "DELETE FROM city WHERE id = {} and name = '{}'".format(id,city)
	q = connection.execute(query)
	print(q)
	connection.commit()
	bot.send_message(chat_id=id, text='The city removed successfully!')
	print('Removed!')

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu



updater.dispatcher.add_handler(CommandHandler('start',start))
updater.dispatcher.add_handler(CommandHandler('weather',weather))
updater.dispatcher.add_handler(CommandHandler('add',add))
updater.dispatcher.add_handler(CommandHandler('stop',stop))
updater.dispatcher.add_handler(CommandHandler('remove', remove))
updater.dispatcher.add_handler(MessageHandler(Filters.text, findweather),group=0)
#updater.dispatcher.add_handler(MessageHandler(Filters.text, jeez),group=2)
updater.dispatcher.add_handler(CallbackQueryHandler(callback))
updater.start_polling()




