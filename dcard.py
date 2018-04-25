import re
import requests
from bs4 import BeautifulSoup

url = 'https://www.dcard.tw/f'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')
dcard_title = soup.find_all('h3', re.compile('PostEntry_title_'))

print('Dcard 熱門前十文章標題：')

for index, item in enumerate(dcard_title[:10]):
  print("{0:2d}. {1}".format(index+1, item.text.strip()))  # strip() 移除字串前後的空白

