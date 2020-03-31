import requests
import misc
import json
from time import sleep
import trello
import films
import telegram

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
        message['callback_data'] = update.get('callback_data').get('data')

    print('message', message)

    return message


def send_message(chat, text, keyboard={}):
    params = {
        'chat_id': chat,
        'text': text,
    }

    if 'inline_keyboard' in keyboard:
        # print('inline keyboard')
        params['reply_markup'] = keyboard

    # print('params', params)
    response = requests.post(url + 'sendMessage', data=params)
    return response


def save_film(list_name, film_name, chat_id):
    print('film_name', film_name)
    movie_list = films.MovieList(film_name).movies
    # print('movie_list', movie_list)

    if len(movie_list) == 1:
        print('one')
        movie = films.Film(film_name)
        movie.get_movie_content()
        board = trello.Board('Для бота')
        name = f'{film_name} (KP - {movie.rating})'
        board_list = trello.List(board.get_board_lists(), list_name)
        card = trello.Card()
        labels_list = []

        for genre in movie.genres:
            if not any(label['name'] == genre for label in board.labels):
                labels_list.append(board.create_label(genre))
            else:
                for label in board.labels:
                    if label['name'] == genre:
                        labels_list.append(label['id'])

        card.post_card(name, movie.plot, board_list.id, labels_list)
    else:
        print('many')
        formatted_list = list(map(lambda m: [{'text': f'{m}', 'callback_data': f'{m}'}], movie_list))

        send_message(chat_id, 'Помоги выбрать', json.dumps({'inline_keyboard': formatted_list}))


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
    test_keyboard = json.dumps({"inline_keyboard": [[{"text": "1", "url": "https://yandex.ru/"}]]})
    send_message(chat_id, 'тест клавиатуры', test_keyboard)


def main():
    update_id = last_update(get_updates_json(url))['update_id']
    board = trello.Board('Для бота')

    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:

            answer = get_message(last_update(get_updates_json(url)))

            chat_id = answer['chat_id']
            # print('answer', answer)

            command = answer['text'] if answer['text'].startswith(bot_name) or answer['text'].startswith('/') else ''

            if command != '':
                print('command')
                if command.find('запомни фильм') != -1:
                    send_message(chat_id, 'Диктуй!')
                elif command.find('посмотрели') != -1:
                    send_message(chat_id, 'Давай название!)')
                elif command.find('тест') != -1:
                    send_test(chat_id)
                else:
                    text = answer['text']
                    send_message(chat_id, 'Ты написал: "' + text + '"')
            elif 'callback_data' in answer:
                print('callback')
                save_film('Не смотрели', answer.get('callback_data'), chat_id)
            elif answer['reply_to_message'] and answer['reply_to_message']['from']['id'] == 550506408:
                print('reply')
                if answer['reply_to_message']['text'] == "Диктуй!":
                    film_name = answer['text'].capitalize()
                    if any(card['name'].find(film_name) != -1 for card in board.get_board_cards()):
                        send_message(chat_id, "Такой уже есть")
                    else:
                        save_film('Не смотрели', film_name, chat_id)
                elif answer['reply_to_message']['text'] == "Давай название!)":
                    film_name = answer['text'].capitalize()
                    move_film('Посмотрели', film_name, chat_id)

            update_id += 1
        sleep(3)


if __name__ == '__main__':
    main()
