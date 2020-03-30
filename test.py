import requests

url = 'https://api.telegram.org/bot550506408:AAFS8jAyuapzVFsrlB9Gu1TWGO6T0BPFS4c/getUpdates'

# proxies = {
#     'http': 'socks5://telega:nNcl1BFJOG0@v1.gpform.pro:31080',
#     'https': 'socks5://telega:nNcl1BFJOG0@v1.gpform.pro:31080'
# }


try:
    response = requests.get(url)
    print(response.json())
except requests.exceptions.ConnectionError:
    response.status_code = "Connection refused"
