import requests
import os


def sendMessage(message):
    token = os.environ['TELEGRAM_TOKEN']
    chatId = os.environ['CHAT_ID']

    telegramUrl = 'https://api.telegram.org/bot' + token + '/sendMessage'
    data = {'chat_id': chatId, 'text': message}
    resp = requests.post(url=telegramUrl, data=data)
    print(resp)
