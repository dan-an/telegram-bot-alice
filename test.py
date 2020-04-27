import requests

url = 'https://api.telegram.org/bot550506408:AAFS8jAyuapzVFsrlB9Gu1TWGO6T0BPFS4c/getUpdates'


try:
    response = requests.get(url)
    print(response.json())
except requests.exceptions.ConnectionError:
    response.status_code = "Connection refused"
