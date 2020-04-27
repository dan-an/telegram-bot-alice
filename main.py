import requests
import misc
import json
from time import sleep
import trello
import films
import random

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
    return results[-1] if len(results) != 0 else None


def get_message(update):
    message_data = update.get('callback_query').get('message') if 'callback_query' in update else update.get('message')
    chat_id = message_data['chat']['id']
    message_text = message_data['text'].lower()
    reply = message_data.get('reply_to_message', None)

    message = {
        'chat_id': chat_id,
        'text': message_text,
        'reply_to_message': reply
    }

    if 'callback_query' in update:
        message['callback_data'] = update.get('callback_query').get('data')

    return message


def send_message(chat, text, reply_markup=None):
    params = {
        'chat_id': chat,
        'text': text,
    }

    if reply_markup is not None:
        params['reply_markup'] = reply_markup

    response = requests.post(url + 'sendMessage', data=params)
    return response


def search_film(chat_id, search_query=None, movie_id=None):
    movie = None

    if search_query:
        movie_list = films.MovieList(search_query).movies

        if len(movie_list) == 0:
            send_message(chat_id, random.choice(misc.bot_replies.get('nothing_found')))
        elif len(movie_list) == 1:
            movie = films.Film(movie_list[0].id)
        else:
            formatted_list = list(map(lambda m: [{'text': f'{m}', 'callback_data': f'{m.id}'}], movie_list))
            send_message(chat_id, f"{random.choice(misc.bot_replies.get('ask_help'))}:",
                         json.dumps({'inline_keyboard': formatted_list}))

    elif movie_id:
        movie = films.Film(movie_id)

    if movie:
        movie.get_movie_content()

    return movie


def save_film(list_name, movie_data, chat_id):
    board = trello.Board('Для бота')
    ratings = ', '.join([f'{key} {value}' for (key, value) in movie_data.ratings.items() if value is not None])
    name = f'{movie_data.title}, {movie_data.year}'

    if len(ratings) != 0:
        name = f'{name} ({ratings})'

    board_list = trello.List(board.get_board_lists(), list_name)
    card = trello.Card()
    labels_list = []

    for genre in movie_data.genres:
        if not any(label['name'] == genre for label in board.labels):
            labels_list.append(board.create_label(genre))
        else:
            for label in board.labels:
                if label['name'] == genre:
                    labels_list.append(label['id'])

    card.post_card(name, movie_data.plot, board_list.id, labels_list)
    send_message(chat_id, "Запомнила")


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


def main():
    update_id = last_update(get_updates_json(url))['update_id']
    board = trello.Board('Для бота')

    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:

            answer = get_message(last_update(get_updates_json(url)))

            chat_id = answer['chat_id']

            command = answer['text'] if bot_name in answer['text'] or answer['text'].startswith('/') else ''

            if command != '':
                if any(request_str in command for request_str in misc.user_requests.get('save_requests')):
                    send_message(chat_id, 'Диктуй!', json.dumps({'force_reply': True}))
                elif any(request_str in command for request_str in misc.user_requests.get('watched_requests')):
                    send_message(chat_id, 'Давай название!)', json.dumps({'force_reply': True}))
                else:
                    send_message(chat_id, f'Ты написал: {answer["text"]}')
            elif 'callback_data' in answer:
                movie_data = search_film(chat_id, movie_id=answer.get('callback_data'))
                save_film('Не смотрели', movie_data, chat_id)
            elif answer['reply_to_message'] and answer['reply_to_message']['from']['id'] == 550506408:
                if answer['reply_to_message']['text'] == "Диктуй!":
                    film_name = answer['text'].capitalize()
                    if any(card['name'].find(film_name) != -1 for card in board.get_board_cards()):
                        send_message(chat_id, "Такой уже есть")
                    else:
                        movie_data = search_film(chat_id, search_query=film_name)
                        if movie_data:
                            save_film('Не смотрели', movie_data, chat_id)
                elif answer['reply_to_message']['text'] == "Давай название!)":
                    film_name = answer['text'].capitalize()
                    move_film('Посмотрели', film_name, chat_id)

            update_id += 1
        sleep(3)


if __name__ == '__main__':
    main()
