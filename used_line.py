# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 16:04:08 2017

@author: thotran

Assume most results used on used-line are used, Use this function only to search for used
"""
import util
from Result import Result
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
#Code in Progress
MAIN_URL='http://www.used-line.com/search/s_index.cfm?search_term='
DELIMITER='+'
   

def extract_results(search_word, condition=None):
    if condition=='new':
        return []
    url=util.create_url(MAIN_URL,search_word,DELIMITER)
    page =urllib.request.urlopen(url)
    soup=BeautifulSoup(page,"html.parser")
    product_grid=soup.find('ul', class_='Products_ul')
    try:
        total_equips=product_grid.find_all('li',class_='Products')
    except:
        return []
    equips=[]
    for equip in total_equips:
        title=equip.find('div', class_='title').find('span').find(text=True).strip()
        equipment=Result(title)
        equipment.url=equip.find('a').get('href')
        equipment.image_src=equip.find('div', class_='Image').find('img').get('src')
        price_text=equip.find('div', class_='price').find_all(text=True)
        equipment.price=util.get_price(''.join(price_text))
        if util.is_valid_price(equipment.price):
            equips.append(equipment)
        if len(equips)>=10:
            return equips
    return equips

def main():
    print((extract_results('centrifuge')))

if __name__=='__main__': main()
