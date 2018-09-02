'''
Created by Abigail Katcoff (complete)
New and Used Equipment
'''
import util
import urllib2
from bs4 import BeautifulSoup
from Result import Result

MAIN_URL='http://www.ebay.com/sch/i.html?_nkw='
DELIMITER= '+'

USED= '&LH_ItemCondition=4'
NEW= '&LH_ItemCondition=1'

def extract_results(search_term, condition=None):
	url=''
	if condition=='new':
		url = util.create_url(MAIN_URL, search_term, DELIMITER) + '&LH_BIN=1' + NEW
	else:
		url = util.create_url(MAIN_URL, search_term, DELIMITER) + '&LH_BIN=1' + USED
	page=urllib2.urlopen(url)
	soup = BeautifulSoup(page,"html.parser")
	table=soup.find('div', id='ResultSetItems')
	try:
		rows=table.findAll('li', class_='sresult lvresult clearfix li')
	except:
		return []
	results=[]
	for row in rows: 
		new_result=Result(row.find('h3', class_="lvtitle").find(text=True))
		new_result.url=row.find('h3', class_="lvtitle").find('a').get('href')
		new_result.image_src=row.find('img', class_='img').get('src')
		new_result.price=util.get_price(row.find('li', class_="lvprice prc").find('span').find(text=True))
		if util.is_valid_price(new_result.price):
			results.append(new_result)
	return results

def main():
    print extract_results("vacuum bump")

if __name__ == "__main__": main()
