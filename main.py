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


def send_message(chat, text, keyboard={}):
    params = {
        'chat_id': chat,
        'text': text,
    }

    if 'inline_keyboard' in keyboard:
        params['reply_markup'] = test_keyboard

    response = requests.post(url + 'sendMessage', data=params)
    return response


def save_film(list_name, film_name):
    movie = films.Film(film_name)
    movie.get_movie_content()
    board = trello.Board('Для бота')
    name = f'{film_name} (KP - {movie.rating})'
    list = trello.List(board.get_board_lists(), list_name)
    card = trello.Card()
    labels_list = []

    for genre in movie.genres:
        if not any(label['name'] == genre for label in board.labels):
            labels_list.append(board.create_label(genre))
        else:
            for label in board.labels:
                if label['name'] == genre:
                    labels_list.append(label['id'])

    card.post_card(name, movie.plot, list.id, labels_list)


def move_film(list_name, film_name, chat_id):
    board = trello.Board('Для бота')
    list = trello.List(board.get_board_lists(), list_name)
    card = trello.Card()
    card_id = next(card for card in board.get_board_cards() if card['name'].find(film_name) != -1)['id']
    film_exists = any(card['name'].find(film_name) != -1 for card in board.get_board_cards())

    if film_exists and all(card['id'].find(card_id) == -1 for card in list.cards):
        card.move_card(card_id, list.id)
        send_message(chat_id, 'Ок записала)')
    elif film_exists:
        send_message(chat_id, 'Я уже в курсе)')
    else:
        send_message(chat_id, 'Слушай, у меня нет такого(')


def send_test(chat_id):
    test_keyboard = {'inline_keyboard': [[{'text': '1'}], [{'text': '1'}], [{'text': '1'}]]}
    send_message(chat_id, 'тест клавиатуры', test_keyboard)


def main():
    update_id = last_update(get_updates_json(url))['update_id']
    board = trello.Board('Для бота')

    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:

            answer = get_message(last_update(get_updates_json(url)))

            chat_id = answer['chat_id']

            command = answer['text'] if answer['text'].startswith(bot_name) or answer['text'].startswith('/') else ''

            if command != '':
                if command.find('запомни фильм') != -1:
                    send_message(chat_id, 'Диктуй!')
                elif command.find('посмотрели') != -1:
                    send_message(chat_id, 'Давай название!)')
                elif command.find('тест') != -1:
                    send_test(chat_id)
                else:
                    text = answer['text']
                    send_message(chat_id, 'Ты написал: "' + text + '"')
            elif answer['reply_to_message'] and answer['reply_to_message']['from']['id'] == 550506408:
                if answer['reply_to_message']['text'] == "Диктуй!":
                    film_name = answer['text'].capitalize()
                    if any(card['name'].find(film_name) != -1 for card in board.get_board_cards()):
                        send_message(chat_id, "Такой уже есть")
                    else:
                        save_film('Не смотрели', film_name)
                        send_message(chat_id, "Запомнила!")
                elif answer['reply_to_message']['text'] == "Давай название!)":
                    film_name = answer['text'].capitalize()
                    move_film('Посмотрели', film_name, chat_id)

            update_id += 1
        sleep(3)


if __name__ == '__main__':
    main()
