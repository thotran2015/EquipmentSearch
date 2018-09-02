# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 15:21:14 2017

@author: thotran
#Sells used and new 
"""
import util
from Result import Result
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup

MAIN_URL='http://www.medwow.com/tag/fronthandler/browse?actions=sales&searchstring='
DELIMITER='%20'


def extract_results(search_word, condition=None):
    url=util.create_url(MAIN_URL,search_word,DELIMITER)
    url= url if condition!="new" else url +'&Condition=5067'
    try:
        soup = util.check_exceptions(url)
        product_grid=soup.find('div', class_='pagebody')
        total_equips=product_grid.find_all('div',class_='el')
    except:
        return []
    equips=[]
    for equip in total_equips:
        # items_details have names of generic device, model, manufacturer bundled together
        items_details=equip.find('div', class_='item_details').find_all(text=True)
        title=' '.join(items_details).strip()
        equipment=Result(title)
        equipment.url=equip.find('div',class_='image').find('a',class_='item_number').get('href')
        equipment.image_src=equip.find('div',class_='image').find('img').get('src')
        price_text=equip.find('div', class_='price').find(text=True) if equip.find('span', class_='price_element')==None else equip.find('span', class_='price_element').find(text=True)
        equipment.price=util.get_price(''.join(price_text))
        if util.is_valid_price(equipment.price):
            equips.append(equipment)
        if len(equips)>=10:
            return equips
    return equips
    
def main():
    print(extract_results('centrifuge'))

if __name__=='__main__': main()
