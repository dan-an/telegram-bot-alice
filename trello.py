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

board_name = "Для бота"

def trello_get_boards(url, params):
  response = requests.get(url + 'members/me/boards', params=params)
  return response.json()

def get_bot_board(board_list, board_name):
  return next(board for board in board_list if board['name'] == board_name)

def get_board_lists(url, params, board_id):
  response = requests.get(url + 'boards/' + board_id + '/lists', params=params)
  return response.json()

def create_card(url, params, list_id, card_name):
  params['idList'] = list_id
  params['name'] = card_name

  requests.post(url + '/cards', params=params)

def main(card_name):

  existing_trello_boards = trello_get_boards(url, params)

  bot_board = get_bot_board(existing_trello_boards, board_name)

  board_lists = get_board_lists(url, params, bot_board['id'])

  target_list = next(list for list in board_lists if list['name'] == 'Не смотрели')

  create_card(url, params, target_list['id'], card_name)