# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 12:32:55 2017

@author: thotran

#Sells used and new equipment
"""
import util
from Result import Result
import urllib2
from bs4 import BeautifulSoup
#Code in Progress  
MAIN_URL='https://www.dotmed.com/listings/search/equipment.html?key='
DELIMITER='+'
    

def extract_results(search_word, condition=None):
    url=util.create_url(MAIN_URL,search_word,DELIMITER)
    url= url + '&cond=used' if condition!='new' else url + '&cond=new'
    page =urllib2.urlopen(url)
    soup=BeautifulSoup(page,"html.parser")
    product_grid=soup.find('div', id='totalListings')
    equips=[]
    try:
        sale_equips=product_grid.find_all('div', class_='listings_table_d') 
    except:
        try:
            sale_equips=product_grid.find_all('div', class_='listings_table_d ') 
        except:
            return []
    for equip in sale_equips:
        title=''.join(equip.find('dt', class_='listing_head').find_all(text=True)).strip()
        equipment=Result(title)
        equipment.url='http://www.dotmed.com'+equip.find('dt', class_='listing_head').find('a').get('href')
        img_tag=equip.find('dd',class_='img')
        if img_tag!=None:
            equipment.image_src=img_tag.find('img').get('src')
        price_tag=equip.find('dl', class_='datePosted').find('p')
        #filters out products with no price or with foreign prices
        if price_tag!=None and 'USD' in ''.join(price_tag.find_all(text=True)):
            equipment.price=util.get_price(''.join(price_tag.find_all(text=True)))
        if util.is_valid_price(equipment.price):
            equips.append(equipment)
        if len(equips)>=10:
            return equips
    return equips
    
def main():
    print extract_results('vacuum bump')
if __name__=='__main__': main()
