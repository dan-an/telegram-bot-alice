import requests

url = "https://api.telegram.org/bot550506408:AAFS8jAyuapzVFsrlB9Gu1TWGO6T0BPFS4c/"


def get_updates_json(request):  
    response = requests.get(request + 'getUpdates')
    return response.json()


def last_update(data):  
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]