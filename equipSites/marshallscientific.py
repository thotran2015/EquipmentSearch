
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 18:06:56 2017

@author: thotran
Marshall Scientific sells used equipment only. 
"""
import util
from Result import Result
from bs4 import BeautifulSoup
import time
import requests 

MAIN_URL="http://www.marshallscientific.com/searchresults.asp?Search="
DELIMITER='+'


def extract_results(search_word, condition=None):
    if condition=="new":
        return []
    url=util.create_url(MAIN_URL,search_word,DELIMITER)
    try:
        soup = util.check_exceptions(url)
        product_grid=soup.find('div', class_='v-product-grid')
        total_equips=product_grid.find_all('div',class_='v-product')
    except:
        return []
    equips=[]
    
    for equip in total_equips:
        title=equip.find('a', class_='v-product__title productnamecolor colors_productname').find(text=True).strip()
        equipment=Result(title)
        equipment.url=equip.find('a',class_='v-product__img').get('href')
        equipment.image_src='http:'+equip.find('img').get('src')
        price_text=equip.find('div', class_='product_productprice').find_all(text=True)
        equipment.price=util.get_price(''.join(price_text))
        if util.is_valid_price(equipment.price):
            equips.append(equipment)
        if len(equips)>=10:
            return equips
    return equips

def main():
    print(extract_results('vacuum'))

if __name__=='__main__': main()
    
    
    
    






    
    
    
    
    
    
    

