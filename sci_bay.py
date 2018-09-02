'''
Created by Abigail Katcoff (complete)
This website only contains used equipment
'''

import urllib.request, urllib.error, urllib.parse
import util
from bs4 import BeautifulSoup
from Result import Result

MAIN_URL= "http://www.sci-bay.com/?s="
DELIMITER= '+'

def extract_results(search_term, condition=None):
	if condition=='new':
		return []
	url=util.create_url(MAIN_URL, search_term, DELIMITER)
	page=urllib.request.urlopen(url)
	soup = BeautifulSoup(page,"html.parser")
	table=soup.find('div', class_='content-area')
	rows= table.findAll("article")

	results=[]
	for row in rows:
		new_result=Result(row.find('h1', class_="entry-title").find("a").find(text=True))
		result_url=row.find('a').get('href')

		#scrape from the result's page
		result_soup=BeautifulSoup(urllib.request.urlopen(result_url),"html.parser")
		new_result.url=result_url
		new_result.price=util.get_price(result_soup.find('span', class_="amount").find(text=True))
		new_result.image_src=result_soup.find('div', class_='images').find('img').get('src')
		if util.is_valid_price(new_result.price):
			results.append(new_result)
			if len(results)==10: return results
	return results

def main():
    results= extract_results("Beckman")
    #Printing the results the usual way gives an error because some elements contain u'2013
    try:
    	print(results)
    except:
	    for result in results:
	    	print(result.title, result.url) 
	    	print(result.price, result.image_src + "\n")

if __name__ == "__main__": main()
