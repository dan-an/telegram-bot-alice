import requests
import misc
import json
from time import sleep

token = misc.token

url = 'https://api.telegram.org/bot' + token + '/'

proxies = {
    'http': 'socks5://telegram:telegram@mxajf.tgproxy.me:1080',
    'https': 'socks5://telegram:telegram@mxajf.tgproxy.me:1080'
}


def get_updates_json(request):
    params = {
        'timeout': 100,
        'offset': None
    }
    response = requests.get(request + 'getUpdates', data=params, proxies=proxies)
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
    response = requests.post(url + 'sendMessage', data=params, proxies=proxies)
    return response

def main():
    update_id = last_update(get_updates_json(url))['update_id']

    answer = get_message(last_update(get_updates_json(url)))

    chat_id = answer['chat_id']
    text = answer['text']

    send_message(chat_id, 'Проверим)')

    # while True:
    #     if update_id == last_update(get_updates_json(url))['update_id']:
    #         send_message(get_chat_id(last_update(get_updates_json(url))), 'а у меня скрипты снова обновились бебебе')
    #         update_id += 1
    #     sleep(1)

if __name__ == '__main__':
    main()