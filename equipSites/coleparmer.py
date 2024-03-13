# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 22:29:01 2017
@author: thotran
Status:Complete
Sell new products only
"""

import util
from Result import Result
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup

MAIN_URL="https://www.coleparmer.com/search?searchterm="
DELIMITER='+'
HOME_URL='https://www.coleparmer.com'

def extract_results(search_word, condition=None):
    url=util.create_url(MAIN_URL,search_word,DELIMITER)
    page =urllib.request.urlopen(url)
    soup=BeautifulSoup(page,"html.parser")
    try:
        product_contents=soup.find_all('div', class_='products-mnbox-content')
    except:
        return []

    results=[]
    for product_content in product_contents:
        equip_url=HOME_URL+product_content.find('a').get('href')
        models_site=BeautifulSoup(urllib.request.urlopen(equip_url),"html.parser")
        model_descriptions=models_site.find_all('td', class_='description')

        for re in model_descriptions:
            result=Result(re.find('div',{'id':'gaProductName'}).find(text=True).strip())
            result.image_src='https:'+re.find('img', class_='lazy').get('data-original')
            result.url=HOME_URL+re.find('a').get('href')
            price_site=BeautifulSoup(urllib.request.urlopen(result.url),"html.parser")
            result.price=util.get_price(price_site.find('div', class_='price-box').find('span', class_='price-range').find(text=True))
            if util.is_valid_price(result.price):
                results.append(result)
            if len(results)>=10:
                return results   
    return results
    
def main():
    print(extract_results('vacuum bump'))

if __name__=='__main__': main()
    
