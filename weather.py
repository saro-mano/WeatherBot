import telebot
import time
import requests
import json
import pprint

bot_token = "909999620:AAGA3pzw8ZPAa2lEM1Zp-pTPoqr719xPZiI"

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands = ['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hey there! Enter a city name to find the weather!')

    
@bot.message_handler(func = lambda msg:msg.text is not None)
def at_answer(message):
	msg = message.text.split()
	temperature = weather(msg[0])
	if temperature != "invalid":
		bot.reply_to(message, 'The temperature today is {}°C'.format(temperature))
	else:
		bot.reply_to(message, 'Please enter a valid city!')
	#bot.reply_to(message, 'https://www.instagram.com/{}'.format(instaid[1:]))

def weather(city):
	try:
		api_address='http://api.openweathermap.org/data/2.5/weather?appid=fe77c384145449cdd1bbf0dc8b027998&q='
		url = api_address + str(city)
		json_data = requests.get(url).json()
		pp = pprint.PrettyPrinter(indent=4) #reference
		temp_in_kelvin = json_data['main']['temp']
		temp_in_cel = int(temp_in_kelvin)-273.15
		return round(temp_in_cel)
	except:
		return "invalid"


while True:
    try:
        bot.polling()
    except Exception:
        exit()
