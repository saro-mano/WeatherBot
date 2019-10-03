import telebot
import time
import requests
import json
import pprint


bot_token = "909999620:AAGA3pzw8ZPAa2lEM1Zp-pTPoqr719xPZiI"

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands = ['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hey there! Type any insta id with @ symbol!')

@bot.message_handler(commands = ['start'])
def send_welcome(message):
    

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(10)

# while True:
#     api_address='http://api.openweathermap.org/data/2.5/weather?appid=fe77c384145449cdd1bbf0dc8b027998&q='
#     city = input('City Name :')
#     url = api_address + city
#     json_data = requests.get(url).json()
#     pp = pprint.PrettyPrinter(indent=4)
#     pp.pprint(json_data)
#     temp_in_kelvin = json_data['main']['temp']
#     temp_in_cel = int(temp_in_kelvin)-273.15
#     print("The temperatur is ",round(temp_in_cel))
#     print("The weather is",json_data['weather'][0]['main'])
