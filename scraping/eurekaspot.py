"""
@author Venita Boodhoo
Website: EurekaSpot
Status: Complete
Comment: Assumes all items are used on this website
"""

import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup

import util
from util import *
from Result import Result

main_url = "http://www.eurekaspot.com"
search_url = "http://www.eurekaspot.com/estore/searchtmp2.cfm?quiksrch_keywords="
DELIMITER ="%20"

def extract_results(item,condition=None):
        results=[]
        if condition != "new":
                search_term=get_good_search_term(item)
                url = create_url(search_url,search_term,DELIMITER)
                soup = util.get_soup(url)
                table = soup.find_all('td',class_='productname')
                for row in table:
                        new_result = Result(row.find('a').text)
                        specific_url = main_url+row.find('a').get('href')
                        new_result.url = re.sub('%2E','.',specific_url)
                        new_result.image_src = main_url+\
                                               soup.find('td',class_='image').find('img').get('src')
                        specific_page = urllib.request.urlopen(new_result.url)
                        new_soup = BeautifulSoup(specific_page,"html.parser")
                        try:
                            new_result.price = get_price(new_soup.find('span',class_='sellprice').text)
                        except:
                            continue
                        #Code to add only functional items
                        description_url = main_url+re.sub(' ','%20',new_soup.find('p',id='name').find('a').get('href'))
                        description_page = urllib.request.urlopen(description_url)
                        description_soup = BeautifulSoup(description_page,"html.parser")

                        functional_tag = description_soup.find(text='Functional:')
                        working = functional_tag.find_next('td').text
                        if "yes" in working.lower() and is_valid_price(new_result.price):
                                results.append(new_result)                                                
                        
        return results

'''
Added by Abigail
search_terms is a string
Finds a term that looks like a model number (contains a digit) and returns that term
If no terms containing digits exist, returns first word 
'''
def get_good_search_term(search_terms):
    terms=search_terms.split()
    for term in search_terms.split():
        if any(char.isdigit() for char in term):
            return term
    return "" if len(terms)==0 else terms[0]

def main():
    print(extract_results("pump HX7400"))

if __name__ == "__main__": main()
