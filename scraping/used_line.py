# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 16:04:08 2017

@author: thotran

Assume most results used on used-line are used, Use this function only to search for used
"""
import threading

import util
from Result import Result
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup

# Code in Progress
MAIN_URL = 'http://www.used-line.com/search/s_index.cfm?search_term='
DELIMITER = '+'


def extract_results(search_word: str, results: list, lock: threading.Lock, stop_event: threading.Event,
                    condition: str = 'used'):
    if condition == 'new':
        return
    url = util.create_url(MAIN_URL, search_word, DELIMITER)
    soup = util.get_soup(url)
    try:
        product_grid = soup.find('div', id="search-content")
        print(product_grid)
        total_equips = product_grid.find_all('li')
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return
    for equip in total_equips:
        try:
            if stop_event.is_set():
                break
            title = equip.find('div', class_='title').find('span').find(text=True).strip()
            if not util.is_close_match(search_word, title):
                continue
            url = equip.find('a').get('href')
            price = equip.find('div', class_='price').text
            price = util.get_price(price)
            img_src = equip.find('div', class_='Image').find('img').get('src')
            result = Result(title, url, price, img_src)
            lock.acquire()
            results.append(result)
            lock.release()
            if len(results) >= 10:
                stop_event.set()
                break
        except Exception as e:
            print(f"Can't get this equip: {e}")
    return


def main():
    lock = threading.Lock()
    stop_event = threading.Event()
    results = []
    extract_results('centrifuge', results, lock, stop_event)
    print(results)


if __name__ == '__main__':
    main()
