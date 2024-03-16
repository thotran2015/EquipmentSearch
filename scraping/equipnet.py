"""
This website sells used equipment
"""
import util
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
from Result import Result

HOME_URL = "http://www.equipnet.com"
MAIN_URL = "http://www.equipnet.com/search/?q="
DELIMITER = "%20"


def extract_results(search_term, condition=None):
	if condition == 'new':
		return []
	url = util.create_url(MAIN_URL, search_term, DELIMITER)
	soup = util.get_soup(url)
	table = soup.find('div', class_="search-results-container")
	rows = table.findAll("div", class_="row")
	results = []
	for row in rows:
		# Extract title
		title_tag = row.find('h6', class_='title listing-title-padding')
		title = title_tag.text.strip() if title_tag else None
		# Extract price
		price_tag = row.find('span', class_='price-amount')
		price = price_tag.text.strip() if price_tag else None
		# Extract URL
		url_tag = row.find('a', href=True)
		url = url_tag['href'] if url_tag else None
		if url and 'http' not in url:
			url = HOME_URL + url
		# Extract image URL
		image_tag = row.find('img', class_='list-view-thumbnail')
		image_url = image_tag['src'] if image_tag else None
		new_result = Result(title)
		new_result.price = util.get_price(price)

		new_result.url = url
		new_result.image_src = image_url
		if util.is_valid_price(new_result.price):
			results.append(new_result)
	return results


def main():
	print(extract_results("Beckman Coulter Biomek Workstation"))


if __name__ == "__main__":
	main()
