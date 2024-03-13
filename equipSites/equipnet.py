'''
Created by Abigail Katcoff (complete)
This website sells used equipment
'''
import util
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
from Result import Result

MAIN_URL= "http://www.equipnet.com/search/?q="
DELIMITER="%20"

def extract_results(search_term, condition=None):
	if condition=='new':
		return []
	url=util.create_url(MAIN_URL, search_term, DELIMITER)
	page=urllib.request.urlopen(url)
	soup = BeautifulSoup(page,"html.parser")
	table=soup.find('div', id='tbl-listings')
	try:
		rows= table.findAll("div", class_="search-row")
		rows[0].find('h3', class_="listing-title").find("a").find(text=True)
	except:
		return []
	results=[]
	for row in rows:
		new_result=Result(row.find('h3', class_="listing-title").find("a").find(text=True))
		new_result.price=util.get_price(row.find('span', class_="listing-price").find(text=True))
		new_result.url=row.find('a').get('href')
		new_result.image_src=row.find('img', class_="search-thumbnail").get('src')
		if util.is_valid_price(new_result.price):
			results.append(new_result)
	return results

def main():
    print(extract_results("Beckman Coulter Biomek Workstation"))

if __name__ == "__main__": main()
