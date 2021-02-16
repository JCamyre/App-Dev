from requests import get
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime


pd.options.display.max_columns = 10

# With the amount I am accessing finviz, would it be easier to make an API?
# Each stock is an object, use .get_news(), .get_price_targets(), etc.

# Make this a class, then for all of these don't need ticker, just do self.ticker

def _find_match(pattern, text):
	match = pattern.search(text)
	return match

def _no_attributes(tag):
	if 'td' in str(tag):
		return tag.has_attr('class') or tag.has_attr('id')

def _get_soup(url):
	response = get(url, headers=HEADERS, timeout=20)
	assert response.status_code == 200
	return BeautifulSoup(response.content, 'lxml')


HEADERS = {'User-Agent': "'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) AppleWebKit/537.36 " # Telling the website what browser I am "using"
							 "(KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'"}
# Price targets
def _price_target(ticker, exchange='NASDAQ'): # Automatically find correct stock exchange
	soup = _get_soup(BASE_URL)
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
	for row in rows:
		row = row.find_all('td')
		date, _, fund, action, pricetarget = [val.get_text() for val in row]
		date = datetime.strptime(date, '%b-%d-%y')
		df_data.append((date, fund, action, pricetarget))

	analyst_price_targets = pd.DataFrame(df_data, columns=['Date', 'Fund', 'Action', 'PriceTarget'])
	analyst_price_targets = analyst_price_targets.set_index('Date')
	return price_target, percentage, analyst_price_targets

# print(_price_target('AAPL'))

# html = soup.prettify("utf-8") Good way to visualize what your Python code is visualizing
# with open('output1.html', 'w', encoding='utf-8') as f:
# 	f.write(str(_price_target('AAPL')))

def _price_predictions(ticker):
	BASE_URL = f'https://www.barchart.com/stocks/quotes/{ticker}/opinion'
	soup = _get_soup(BASE_URL)

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

def _ta_indictators(ticker, exchange='NASDAQ'): # Loads wrong page
	BASE_URL = f'https://www.tradingview.com/symbols/{exchange}-{ticker}/technicals/'
	soup = _get_soup(BASE_URL)

	# Buy or sell (Summary, Oscillators, Moving Averages)
	s = soup.find_all('div', {'class': 'speedometerWrapper-1SNrYKXY'})
	print(s)

	# Oscillators
	oscillators = soup.find('div', {'class': 'container-2w8ThMcC tableWithAction-2OCRQQ8y'})
	# with open('output1.html', 'w', encoding='utf-8') as file:
	# 	file.write(str(soup.prettify('utf-8')))

# _ta_indictators('AAPL')

def _sentiments_news(ticker): # Returns news articles curated via Finviz
	BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
	soup = _get_soup(BASE_URL)

	table = soup.find('table', {'class': 'fullview-news-outer'})
	rows = table.find_all('tr')
	df_data = []
	for row in rows:
		date = row.find('td', {'align': 'right'})
		article = row.find('td', {'align': 'left'})
		link = article.find('a')['href']
		df_data.append((date.get_text(), article.get_text(), link))
	df = pd.DataFrame(df_data, columns=['Time', 'Headline', 'Link'])
	return df

# print(_sentiments_news('AAPL'))

def _financials(ticker): # OMEGALUL
	BASE_URL = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'

def _short_selling(ticker):
	BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
	soup = _get_soup(BASE_URL)

	labels = soup.find_all('td', {'class': 'snapshot-td2-cp'})
	values = soup.find_all('td', {'class': 'snapshot-td2'})
	return labels[16].get_text(), values[16].get_text(), labels[22].get_text(), values[22].get_text()

_short_selling('AAPL')

def _put_call_ratio(ticker):
	BASE_URL = f'https://www.alphaquery.com/stock/{ticker}/volatility-option-statistics/120-day/put-call-ratio-oi'
	soup = _get_soup(BASE_URL)

	ratio_volume = soup.find('tr', {'id': 'indicator-put-call-ratio-volume'})
	ratio_open_interest = soup.find('tr', {'id': 'indicator-put-call-ratio-oi'})
	forward_price = soup.find('tr', {'id': 'indicator-forward-price'})
	call_breakeven_price = soup.find('tr', {'id': 'indicator-call-breakeven'})
	put_breakeven_price = soup.find('tr', {'id': 'indicator-put-breakeven'})
	option_breakeven_price = soup.find('tr', {'id': 'indicator-option-breakeven'})

	return ratio_volume, ratio_open_interest, forward_price, call_breakeven_price, put_breakeven_price, option_breakeven_price

def _find_competition(ticker):
	BASE_URL = f'https://finviz.com/quote.ashx?t={ticker}'
	soup = _get_soup(BASE_URL)

	td = soup.find_all('td', {'class': 'fullview-links'})[1]
	sectors = td.find_all('a', {'class': 'tab-link'})
	sector_urls = ([str('https://finviz.com/' + i['href']) for i in sectors])
	print(sector_urls)

_find_competition('AAPL')

def _insider_trading(ticker):
	pass