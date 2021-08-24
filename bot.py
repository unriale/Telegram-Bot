import telebot
import time
from config import open_weather_token, telebot_token
import requests
from pprint import pprint
import datetime


bot_token = telebot_token
bot = telebot.TeleBot(token=bot_token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome!")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Some help commands")


@bot.message_handler(func=lambda msg: msg.text is not None and '@' in msg.text)
def at_answer(message):
    bot.reply_to(message, "What should I say")
    get_weather("Lviv", open_weather_token)


def get_weather(city, weather_token):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        pprint(data)

        city = data["name"]
        temp = data["main"]["temp"]
        temp_max = data["main"]["temp_max"]
        temp_min = data["main"]["temp_min"]
        description = data["weather"][0]["description"]
        main_info = data["weather"][0]["main"]
        wind_speed = data["wind"]["speed"]
        sunsrise_timestamp = datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(
            data["sys"]["sunset"])
        print(
            f"City: {city}, temp:{temp}, main_info: {main_info},  wind_speed={wind_speed}, sunsrise={sunsrise_timestamp}")

    except Exception as ex:
        print(ex)


bot.polling()

# while True:
#     try:
#         bot.polling()
#     except Exception:
#         time.sleep(15)
