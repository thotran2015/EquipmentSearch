# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 22:29:01 2017

@author: thotran
Status:Complete
Website with New products
"""
import util
from Result import Result
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import requests

MAIN_URL='https://www.ika.com/en/Products-Lab-Eq/'
r = requests.get(MAIN_URL, timeout = 4)
DELIMITER='/'
HOME_URL='http://www.ika.com'

    
def extract_results(search_word,condition=None):
    url=util.create_url(MAIN_URL,search_word, DELIMITER)
    try:
        soup = util.check_exceptions(url)
        product_table=soup.find('table', class_='table_content')
        result_links=product_table.find_all('a')
    except:
        return []
        
    equips=[]
    for link in result_links:
        product_url=HOME_URL+link.get('href')
        product_page_content=BeautifulSoup(urllib.request.urlopen(product_url),"html.parser")
        title=''.join(product_page_content.find('div', class_='product_left').find('h1').find_all(text=True)).strip()
        equipment=Result(title)
        equipment.url=product_url
        equipment.image_src=HOME_URL+product_page_content.find('img',{"id": "big_product_img"}).get('src')
        equipment.price=util.get_price(product_page_content.find('div', class_='pr_price2').find(text=True))
        if util.is_valid_price(equipment.price):
            equips.append(equipment)
        if len(equips)>=10:
            return equips
    return equips

def main():
    print(extract_results('vial'))

if __name__=='__main__': main()
    