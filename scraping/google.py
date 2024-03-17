"""
New and Used Equipment
"""

import util
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
from Result import Result
import requests

HOME_URL = 'https://www.google.com'
MAIN_URL = 'https://www.google.com/search?output=search&tbm=shop&q='
DELIMITER = '+'


def extract_results(search_term, condition=None):
	url = util.create_url(MAIN_URL, search_term, DELIMITER)
	url = url + '&tbs=vw:l,mr:1,new:1' if condition == 'new' else url
	print("url: ", url)
	headers = {
			'Connection': 'keep-alive',
			'Accept': 'text/html',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
	}

	r = requests.get(url, timeout=5, headers=headers)
	soup = BeautifulSoup(r.content, "html.parser")
	table = soup.find('div', id='search')
	try:
		rows = table.findAll('div', class_='psli')
	except:
		return []

	results = []
	for row in rows:
		if condition != 'new' and ('used' not in str(row.find('span', class_='price'))):
			# skip over items that do not say "used" when searching for used items
			continue
		if "eBay" in str(row.find('div', class_='_tyb shop__secondary').text):
			# many google results overlap with eBay. Do not include these.
			continue
		new_result = Result(row.find('a', class_='pstl').find(text=True))
		new_result.url = HOME_URL + row.find('a', class_='pstl').get('href')
		new_result.price = util.get_price(row.find('span', class_='price').b.find(text=True))
		if util.is_valid_price(new_result.price):
			results.append(new_result)
	return results


def main():
	print(extract_results("centrifuge", "new"))


if __name__ == "__main__": main()
