import requests
from bs4 import BeautifulSoup
req = requests.get('http://www.soundplayer.co.kr')

html = req.text

header = req.headers

status = req.status_code

is_ok = req.ok

print(html)

