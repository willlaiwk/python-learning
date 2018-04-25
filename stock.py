import re
import requests
from bs4 import BeautifulSoup

input_stock_no = input("請輸入股票代號：")

url1 = 'https://tw.stock.yahoo.com/q/q?s=' + input_stock_no # 名稱, 編號, 成交價
url2 = 'https://tw.stock.yahoo.com/d/s/company_' + input_stock_no + '.html' #最新四季每股盈餘

resp1 = requests.get(url1)
soup1 = BeautifulSoup(resp1.text, 'html.parser')
stock = soup1.find('a', href='/q/bc?s=' + input_stock_no)

if(stock is None):
  print('查無此股票代號!')
else:
  table_td = soup1.find_all('td', bgcolor="#FFFfff")

  stock_no = stock.text[0:4]  # 股票代號
  stock_name = stock.text[4:] # 股票名稱
  price_deal = table_td[1].text # 當前成交價
  price_yesterday = table_td[6].text  # 昨日收盤價

  resp2 = requests.get(url2)
  soup2 = BeautifulSoup(resp2.text, 'html.parser')
  trs = soup2.find('td', string=re.compile("最新四季每股盈餘")).parent.parent.find_all('tr')[1:5]

  EPS_average = 0.0

  for index, item in enumerate(trs):
    EPS_average += float(trs[index].find_all('td')[3].text.split('元')[0])

  EPS_average = EPS_average / 4   # 過去4季平均每股盈餘(EPS)
  PER = float(price_deal) / EPS_average  # 本益比 = 股價 / EPS

  print('# {0} ({1})'.format(stock_name, stock_no))
  print('-----------------------')
  print('成交： {0}'.format(price_deal))
  print('昨收： {0}'.format(price_yesterday))
  print('平均EPS： {0}'.format(EPS_average))
  print('本益比： {0}'.format(PER))
