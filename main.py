import os
import telebot
from telebot import types
import requests

bot = telebot.TeleBot(os.getenv('SHAZAM_TG_API_TOKEN'))
API_KEY = os.getenv('SHAZAM_API_KEY')

url = "https://shazam.p.rapidapi.com/search"


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    bot.send_message(message.chat.id, 'Я - <b>бот</b>, который находит песню по словам, что ты успел запомнить ;)',
                     parse_mode='html')
    bot.send_message(message.chat.id, 'Пришли фрагмент, чтобы я постарался найти')


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text.lower()[0] in 'abcdefghijklmnopqrstuvwxyz':
        querystring = {"term": message.text, "locale": "en-US", "offset": "0", "limit": "7"}

        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "shazam.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        # for i in range(len(response.json()['tracks']['hits'][0])):
        artist = response.json()['artists']['hits'][0]['artist']['name']
        song = response.json()['tracks']['hits'][0]['track']['title']
        bot.send_message(message.chat.id, f'{artist} - {song}')
    else:
        querystring = {"term": message.text, "locale": "ru-RU", "offset": "0", "limit": "7"}

        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "shazam.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        # for i in range(len(response.json()['tracks']['hits'][0])):
        artist = response.json()['artists']['hits'][0]['artist']['name']
        song = response.json()['tracks']['hits'][0]['track']['title']
        bot.send_message(message.chat.id, f'{artist} - {song}')


bot.infinity_polling()
