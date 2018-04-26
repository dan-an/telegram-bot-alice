import requests
from time import sleep

url = "https://api.telegram.org/bot550506408:AAFS8jAyuapzVFsrlB9Gu1TWGO6T0BPFS4c/"

proxies = {
    'http': 'socks5://telegram:telegram@ottgm.tgproxy.me:1080',
    'https': 'socks5://telegram:telegram@ottgm.tgproxy.me:1080'
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
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    print(chat_id)
    return chat_id

def send_message(chat, text):
    params = {
        'chat_id': chat,
        'text': text
    }
    response = requests.post(url + 'sendMessage', data=params, proxies=proxies)
    print(response)
    return response

def main():
    update_id = last_update(get_updates_json(url))['update_id']
    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:
            send_message(get_chat_id(last_update(get_updates_json(url))), 'а у меня скрипты снова обновились бебебе')
            update_id += 1
        sleep(1)

if __name__ == '__main__':
    main()