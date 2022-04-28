import requests
import os
import json

from dotenv import load_dotenv

load_dotenv()

def sendMessage(message, reply=None):
    token = os.environ['TELEGRAM_TOKEN']
    chatId = os.environ['CHAT_ID']

    telegramUrl = 'https://api.telegram.org/bot' + token + '/sendMessage'
    data = {'chat_id': chatId, 'text': message}

    if reply != None:
        inline_keyboard = [[]]

        for r in reply:
            inline_keyboard[0].append({
                'text': r,
                'callback_data': r
            })

        data['reply_markup'] = json.dumps({
            'inline_keyboard': inline_keyboard
        })


    requests.post(url=telegramUrl, data=data)
