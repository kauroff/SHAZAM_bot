import os
import telebot
from telebot import types
import requests
import json
import time

bot = telebot.TeleBot(os.getenv('SHAZAM_TG_API_TOKEN'))
API_KEY = os.getenv('SHAZAM_API_KEY')

url = "https://shazam.p.rapidapi.com/search"


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! \U0001F44B')
    bot.send_message(message.chat.id, 'Я - <b>бот</b> \U0001F47E, который находит треки',
                     parse_mode='html')
    bot.send_message(message.chat.id,
                     'Пришли фрагмент текста, исполнителя или голосовое сообщение со звучанием (10-20 секуyд), чтобы я постарался найти')


@bot.message_handler(content_types=['text'])
def message_info(message):
    bot.send_message(message.chat.id, 'Дай мне буквально пару секунд...')
    if message.text.lower()[0] in 'abcdefghijklmnopqrstuvwxyz':
        querystring = {"term": message.text, "locale": "en-US", "offset": "0", "limit": "7"}

    else:
        querystring = {"term": message.text, "locale": "ru-RU", "offset": "0", "limit": "7"}

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "shazam.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    try:
        type(len(response.json()['tracks']['hits'])) == int
        bot.send_message(message.chat.id, 'Вот какие песни мне удалось найти:')
        for i in range(len(response.json()['tracks']['hits'])):
            # photo = response.json()['tracks']['hits'][i]['track']['share']['image']
            text = response.json()['tracks']['hits'][i]['track']['share']['subject']
            bot.send_message(message.chat.id, text)
            # bot.send_photo(message.chat.id, photo, text)
            # bot.send_audio(message.chat.id, response.json()['tracks']['hits'][i]['hub']['actions'][1]['uri'])
    except(KeyError):
        bot.send_message(message.chat.id,
                         'Не смог ничего найти \U0001F614')
    finally:
        bot.send_message(message.chat.id, 'Попробуем еще?')


@bot.message_handler(content_types=['voice'])
def message_audio(message):
    bot.send_message(message.chat.id, 'Дай мне буквально пару секунд...')
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get(
        'https://api.telegram.org/file/bot{0}/{1}'.format(os.getenv('SHAZAM_TG_API_TOKEN'), file_info.file_path))

    with open('voice.ogg', 'wb') as f:
        f.write(file.content)
    with open('voice.ogg', 'rb') as f:
        api_url = 'https://audiotag.info/api'
        apikey = os.getenv('AUDIO_API_KEY')
        payload = {'action': 'identify', 'apikey': apikey}
        result = requests.post(api_url, data=payload, files={'file': f})
        try:
            token = json.loads(result.text)['token']
            n = 1;
            while n < 100:
                time.sleep(0.5);
                n += 1;
                payload = {'action': 'get_result', 'token': token, 'apikey': apikey}
                result = requests.post(api_url, data=payload)
                track, group = json.loads(result.text)['data'][0]['tracks'][0][0], \
                    json.loads(result.text)['data'][0]['tracks'][0][1]
                break
            bot.send_message(message.chat.id, f'{track} - {group}')
            # if track.lower()[0] in 'abcdefghijklmnopqrstuvwxyz':
            #     querystring = {"term": track, "locale": "en-US", "offset": "0"}
            #
            # else:
            #     querystring = {"term": track, "locale": "ru-RU", "offset": "0"}
            #
            # headers = {
            #     "X-RapidAPI-Key": API_KEY,
            #     "X-RapidAPI-Host": "shazam.p.rapidapi.com"
            # }
            #
            # response = requests.get(url, headers=headers, params=querystring)
            # photo = response.json()['tracks']['hits'][0]['track']['share']['image']
            # text = response.json()['tracks']['hits'][0]['track']['share']['subject']
            # bot.send_photo(message.chat.id, photo, text)

        except(KeyError):
            bot.send_message(message.chat.id,
                             'Не смог ничего найти \U0001F614')
        finally:
            bot.send_message(message.chat.id, 'Попробуем еще?')


bot.infinity_polling()
