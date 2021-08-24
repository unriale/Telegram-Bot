import telebot
import time
from config import open_weather_token, telebot_token, hello_messages, emoji
import requests
from pprint import pprint
import datetime
import random

bot_token = telebot_token
bot = telebot.TeleBot(token=bot_token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, f"{random.choice(hello_messages)} {random.choice(emoji)}")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Some help commands")


@bot.message_handler(func=lambda msg: msg.text is not None and '@' in msg.text)
def at_answer(message):
    bot.reply_to(message, "What should I say")


@bot.message_handler(commands=['weather'])
def get_weather(message):
    try:
        city_list = list(filter(lambda x: '/' not in x, message.text.split()))
        city_words = ' '.join([str(item) for item in city_list])
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_words}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

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
        result = f"\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n{main_info}, {round(temp)}°С\n{description}\nWind speed: {wind_speed}\nSunrise: {sunsrise_timestamp.strftime('%H:%M')}\nSunset: {sunset_timestamp.strftime('%H:%M')}"

        bot.reply_to(message, result)

    except Exception as ex:
        print(ex)


bot.polling()

# while True:
#     try:
#         bot.polling()
#     except Exception:
#         time.sleep(15)
