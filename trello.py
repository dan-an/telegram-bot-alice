import requests
import misc
import json

trello_token = misc.token['trello']
trello_api_key = misc.api_key['trello']

url = 'https://api.trello.com/1/'

params = {
    'key': trello_api_key,
    'token': trello_token
}


class Board:
    def __init__(self, name):
        self.board_name = name
        self.id = None
        self.lists = None
        self.cards = None
        self.labels = None
        self.get_bot_board()

    def get_bot_board(self):
        response = requests.get(url + 'members/me/boards', params=params)
        board_list = response.json()
        bot_board = next(board for board in board_list if board['name'] == self.board_name)
        self.id = bot_board['id']
        self.get_labels()
        return bot_board

    def get_board_lists(self):
        response = requests.get(url + 'boards/' + self.id + '/lists', params=params)
        self.lists = response.json()
        return response.json()

    def get_board_cards(self):
        response = requests.get(url + 'boards/' + self.id + '/cards', params=params)
        self.lists = response.json()
        return response.json()

    def get_labels(self):
        raw_labels = requests.get(f'{url}/boards/{self.id}/labels/', params=params).json()
        self.labels = [label for label in raw_labels if label['name'] != '']

    def create_label(self, label_name):
        query = {
            'name': label_name,
            'color': None,
            'idBoard': self.id,
        }

        response = requests.post(f'{url}labels/', params={**query, **params})
        self.get_labels()
        return response.json()['id']


class List:
    def __init__(self, board_lists, list_name):
        self.name = list_name
        self.id = next(list for list in board_lists if list['name'] == self.name)['id']


class Card:
    def __init__(self):
        self.name = None
        self.description = None

    def post_card(self, name, description, list_id, labels):
        query = {
            **params,
            'idList': list_id,
            'name': name,
            'desc': description,
            'idLabels': ','.join(labels)
        }

        requests.post(f'{url}/cards', params=query)

    def move_card(self, card_id, list_id):
        print('move')
        query = {
            **params,
            'idList': list_id,
        }

        requests.put(f'{url}/cards/{card_id}', params=query)



