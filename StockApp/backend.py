from requests import get
from bs4 import BeautifulSoup
import re

def _find_match(pattern, text):
	match = pattern.search(text)
	return match

def _no_attributes(tag):
	if 'td' in str(tag):
		return tag.has_attr('class') or tag.has_attr('id')

HEADERS = {'User-Agent': "'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 " # Telling the website what browser I am "using"
							 "(KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'"}
# Price targets
def _price_target(ticker, exchange='NASDAQ'):
	BASE_URL = f'https://www.marketbeat.com/stocks/{exchange}/{ticker}/price-target/'
	response = get(BASE_URL, headers=HEADERS, timeout=20)

	soup = BeautifulSoup(response.content, 'lxml')
	table = soup.find('table', {'class': "scroll-table"})
	# price_target = soup.find('table', {'class': 'scroll-table'})
	_pattern = re.compile(r'Price Target: \$\d{1,3}\.\d\d')
	return _find_match(_pattern, table.get_text()).group(0)

print(_price_target('A', exchange='NYSE'))

# html = soup.prettify("utf-8") Good way to visualize what your Python code is visualizing
# with open('output1.html', 'w', encoding='utf-8') as f:
# 	f.write(str(_price_target('AAPL')))
