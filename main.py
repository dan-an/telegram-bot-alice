import requests
import misc
import json
from time import sleep
import trello
import films

telegram_token = misc.token['telegram']

bot_name = misc.bot_name['telegram']

url = 'https://api.telegram.org/bot' + telegram_token + '/'

proxies = {
    'http': 'socks5://telega:nNcl1BFJOG0@v1.gpform.pro:31080',
    'https': 'socks5://telega:nNcl1BFJOG0@v1.gpform.pro:31080'
}


def get_updates_json(request):
    params = {
        'timeout': 100,
        'offset': None
    }
    response = requests.get(request + 'getUpdates', data=params)

    return response.json()


def last_update(data):
    results = data['result']
    return results[-1]


def get_message(update):
    chat_id = update['message']['chat']['id']
    message_text = update['message']['text'].lower()
    reply = update['message'].get('reply_to_message', None)

    message = {
        'chat_id': chat_id,
        'text': message_text,
        'reply_to_message': reply
    }

    return message


def send_message(chat, text):
    params = {
        'chat_id': chat,
        'text': text
    }
    response = requests.post(url + 'sendMessage', data=params)
    return response


def save_film(list_name, film_name):
    movie = films.Film(film_name)
    movie.get_movie_content()
    board = trello.Board('Для бота')
    name = f'{film_name} (KP - {movie.rating})'
    list = trello.List(board.get_board_lists(trello.url, trello.params), list_name)
    card = trello.Card(name, movie.plot)
    labels_list = []

    for genre in movie.genres:
        print(genre)
        if not any(label['name'] == genre for label in board.labels):
            labels_list.append(board.create_label(trello.url, trello.params, genre))
        else:
            for label in board.labels:
                if label['name'] == genre:
                    labels_list.append(label['id'])

    print('labels_list', labels_list)

    card.post_card(trello.url, trello.params, list.id, labels_list)


def main():
    update_id = last_update(get_updates_json(url))['update_id']

    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:

            answer = get_message(last_update(get_updates_json(url)))

            chat_id = answer['chat_id']

            if answer['text'].startswith(bot_name) or answer['text'].startswith('/'):
                if answer['text'].find('запомни фильм') != -1:
                    send_message(chat_id, 'Диктуй!')
                else:
                    text = answer['text']
                    send_message(chat_id, 'Ты написал: "' + text + '"')
            elif answer['reply_to_message'] and answer['reply_to_message']['from']['id'] == 550506408 and \
                    answer['reply_to_message']['text'] == "Диктуй!":
                save_film('Не смотрели', answer['text'].capitalize())
                send_message(chat_id, "Запомнила!")

            update_id += 1
        sleep(3)


if __name__ == '__main__':
    main()
