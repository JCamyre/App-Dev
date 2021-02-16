from requests import get
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime

def _find_match(pattern, text):
	match = pattern.search(text)
	return match

def _no_attributes(tag):
	if 'td' in str(tag):
		return tag.has_attr('class') or tag.has_attr('id')

HEADERS = {'User-Agent': "'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 " # Telling the website what browser I am "using"
							 "(KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'"}
# Price targets
def _price_target(ticker, exchange='NASDAQ'): # Automatically find correct stock exchange
	BASE_URL = f'https://www.marketbeat.com/stocks/{exchange}/{ticker}/price-target/'
	response = get(BASE_URL, headers=HEADERS, timeout=20)

	soup = BeautifulSoup(response.content, 'lxml')
	table = soup.find('table', {'class': "scroll-table"})
	# price_target = soup.find('table', {'class': 'scroll-table'})
	_pattern = re.compile(r'Price Target: \$\d{1,3}\.\d\d')
	price_target = _find_match(_pattern, table.get_text()).group(0)
	_pattern = re.compile(r'\d{1,3}\.\d\d\% \w{6,8}')
	percentage = _find_match(_pattern, table.get_text()).group(0)

	BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
	response = get(BASE_URL, headers=HEADERS, timeout=20)
	soup = BeautifulSoup(response.content, 'lxml')
	table = soup.find('table', {'class': "fullview-ratings-outer"})
	rows = table.find_all('td', {'class': 'fullview-ratings-inner'})
	df_data = []
	print(table)
	for row in rows:
		date, fund, action, _, _, pricetarget = row.get_text().split()
		date = datetime.strptime(date, '%b-%d-%y')[:9]
		df_data.append((date, fund, action, pricetarget))
	analyst_price_targets = pd.DataFrame(df_data, columns=['Date', 'Fund', 'Action', 'PriceTarget'])
	analyst_price_targets = analyst_price_targets.set_index('Date')
	return price_target, percentage, analyst_price_targets

print(_price_target('AAPL'))

# html = soup.prettify("utf-8") Good way to visualize what your Python code is visualizing
# with open('output1.html', 'w', encoding='utf-8') as f:
# 	f.write(str(_price_target('AAPL')))

def _price_predictions(ticker):
	BASE_URL = f'https://www.barchart.com/stocks/quotes/{ticker}/opinion'
	response = get(BASE_URL, headers=HEADERS, timeout=20)
	soup = BeautifulSoup(response.text, 'lxml')
	table = soup.find('table', {'data-ng-class': "{'hide': currentView !== 'strengthDirection'}"})
	titles = soup.find_all('tr', {'class': 'indicator-title'})
	titles = [i.get_text() for i in titles]
	data = soup.find_all('tr', {'class': 'indicator-item'})
	data = [i.get_text() for i in data]
	data = data[len(data)//2 + 1:]
	df_data = []
	for i in data:
		signal, strength, direction = i.split()[-3:]
		indictator = ' '.join(i.split()[:-3])
		df_data.append((indictator, signal, strength, direction))
	df = pd.DataFrame(df_data, columns=['Indictator', 'Signal', 'Strength', 'Direction'])
	print(df.head())


