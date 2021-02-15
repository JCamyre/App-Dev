from requests import get
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': "'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 " # Telling the website what browser I am "using"
							 "(KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'"}
# Price targets
def price_target(ticker, exchange='NASDAQ'):
	BASE_URL = f'https://www.marketbeat.com/stocks/{exchange}/{ticker}/price-target/'
	response = get(BASE_URL, headers=HEADERS, timeout=20)
	assert response.status_code == 200
	soup = BeautifulSoup(response.content, 'lxml')
	return soup 

print(price_target('AAPL'))
