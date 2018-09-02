"""
@author Venita Boodhoo
Website: NewLifeScientific
Status: Complete
Note: Assumes all items are used
"""

import urllib2
from bs4 import BeautifulSoup
from util import *
from Result import Result

MAIN_URL = "http://newlifescientific.com"
SEARCH_URL = "http://newlifescientific.com/search?q="
DELIMITER = "+"

def extract_results(item,condition=None):
        results = []
        if condition != 'new':
                page = urllib2.urlopen(create_url(SEARCH_URL,item,DELIMITER))
                soup = BeautifulSoup(page,"html.parser" )
                #See if page has data
                try:
                        table = soup.find_all('li',class_='item')
                except:
                        return results
                
                for row in table:
                        new_result = Result(row.find('a').get('title'))
                        new_result.url = MAIN_URL+row.find('a').get('href')
                        new_result.price = get_price(row.find('span',class_='price').text)
                        new_result.image_src = row.find('img').get('src')
                        
                        specific_page = urllib2.urlopen(new_result.url)
                        new_soup = BeautifulSoup(specific_page,"html.parser")
                        item_condition = new_soup.find('div',class_='box-collateral-content').find('div',class_='std').text
                        #Checking for matching conditions
                        bad_condition_types = ['bad','poor','not working','broken','not functional']
                        if condition.lower() != "new":
                                #Only add working good equipment
                                for type_word in bad_condition_types:
                                        if type_word not in item_condition and is_valid_price(new_result.price):
                                                results.append(new_result)
                                                break
                
        return results

def main():
    print extract_results("balance scale")

if __name__ == "__main__": main()
