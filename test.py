import requests

url = 'https://api.telegram.org/bot550506408:AAFS8jAyuapzVFsrlB9Gu1TWGO6T0BPFS4c/getUpdates'

proxies = {
    'http': 'socks5://telegram:telegram@gqbyp.teletype.live:1080',
    'https': 'socks5://telegram:telegram@gqbyp.teletype.live:1080'
}


try:
    response = requests.get(url, proxies=proxies)
    print(response.json())
except requests.exceptions.ConnectionError:
    response.status_code = "Connection refused"