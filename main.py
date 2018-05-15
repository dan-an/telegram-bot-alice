import requests
import misc
import json
from time import sleep
from trello import main as save_film

telegram_token = misc.token['telegram']

bot_name = misc.bot_name['telegram']

url = 'https://api.telegram.org/bot' + telegram_token + '/'

proxies = {
    'http': 'socks5://telegram:telegram@xznjl.teletype.live:1080',
    'https': 'socks5://telegram:telegram@xznjl.teletype.live:1080'
}

def get_updates_json(request):
    params = {
        'timeout': 100,
        'offset': None
    }
    response = requests.get(request + 'getUpdates', data=params)
    print(response)
    return response.json()


def last_update(data):
    results = data['result']
    return results[-1]


def get_message(update):

    chat_id = update['message']['chat']['id']
    message_text = update['message']['text']

    message = {
        'chat_id': chat_id,
        'text': message_text
    }

    return message

def send_message(chat, text):
    params = {
        'chat_id': chat,
        'text': text
    }
    response = requests.post(url + 'sendMessage', data=params)
    return response

def main():
    update_id = last_update(get_updates_json(url))['update_id']

    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:

            answer = get_message(last_update(get_updates_json(url)))

            chat_id = answer['chat_id']

            if answer['text'].startswith(bot_name) or answer['text'].startswith('/') :
                if answer['text'].find('запомни фильм') != -1:
                    send_message(chat_id, 'Диктуй!')
                else:
                    text = answer['text']
                    send_message(chat_id, 'Ты написал: "' + text + '"')
            if answer['reply_to_message'] and answer['reply_to_message']['from']['id'] == 550506408 and answer['reply_to_message']['text'] == "Диктуй!":
                save_film(answer['text'])
                send_message(chat_id, "Запомнила!")

            update_id += 1
        sleep(3)

if __name__ == '__main__':
    main()