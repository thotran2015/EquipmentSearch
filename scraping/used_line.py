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

# Code in Progress
MAIN_URL = 'http://www.used-line.com/search/s_index.cfm?search_term='
DELIMITER = '+'


def extract_results(search_word, condition=None):
    if condition == 'new':
        return []
    url = util.create_url(MAIN_URL, search_word, DELIMITER)
    soup = util.get_soup(url)
    results = []
    try:
        product_grid = soup.find('div', id="main_searchResulstPanel")
        print(product_grid)
        total_equips = product_grid.find_all('li')
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return results
    for equip in total_equips:
        try:
            title = equip.find('div', class_='title').find('span').find(text=True).strip()
            url = equip.find('a').get('href')
            price = equip.find('div', class_='price').text
            price = util.get_price(price)
            img_src = equip.find('div', class_='Image').find('img').get('src')
            result = Result(title, url, price, img_src)
            results.append(result)
        except Exception as e:
            print(f"Can't get this equip: {e}")

        if len(results) >= 10:
            return results
    return results


def main():
    print((extract_results('centrifuge')))


if __name__ == '__main__':
    main()
