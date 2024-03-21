# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 22:29:01 2017
@author: thotran
Status:Complete
Sell new products only
"""

import util
from Result import Result
import threading

MAIN_URL = "https://www.coleparmer.com/search?searchterm="
DELIMITER = '+'
HOME_URL = 'https://www.coleparmer.com'


def extract_results(search_word: str, results: list, lock: threading.Lock, stop_event: threading.Event,
                    condition: str = 'used'):
    url = util.create_url(MAIN_URL, search_word, DELIMITER)
    print(url)
    soup = util.get_soup(url)
    try:
        product_list_tag = soup.find('div', class_='products-list-section')
        products = product_list_tag.find_all('li')
    except Exception as e:
        print("Error: ", e)
        return

    for p in products:
        try:
            # Check if stop event is set
            if stop_event.is_set():
                break
            title = p.find('a').get('title')
            if not util.is_close_match(search_word, title):
                continue
            url = HOME_URL + p.find('a').get('href')
            img_src = p.find('img', class_='lazy').get('data-original')
            price_range = p.find('span', class_='price-range')
            if price_range.find('span', itemprop='lowPrice'):
                price = price_range.find('span', itemprop='lowPrice').get('content')
            else:
                price = price_range.text
            price = util.get_price(price)
            new_result = Result(title, url, price, img_src)
            # Acquire lock to safely update the results dictionary
            lock.acquire()
            results.append(new_result)
            lock.release()
            if len(results) >= util.MAX_RESULTS:
                stop_event.set()
                break
        except Exception as e:
            print("Error for product: ", p, e)
    return


def main():
    lock = threading.Lock()
    stop_event = threading.Event()
    results = []
    extract_results('vacuum bump', results, lock, stop_event)
    print(results)


if __name__ == '__main__':
    main()
