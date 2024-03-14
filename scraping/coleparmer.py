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

MAIN_URL = "https://www.coleparmer.com/search?searchterm="
DELIMITER = '+'
HOME_URL = 'https://www.coleparmer.com'


def extract_results(search_word, condition=None):
    url = util.create_url(MAIN_URL, search_word, DELIMITER)
    soup = util.check_exceptions(url)
    results = []
    try:
        product_list_tag = soup.find('div', class_='products-list-section')
        products = product_list_tag.find_all('li')
    except Exception as e:
        print("Error: ", e)
        return results

    for p in products:
        try:
            url = HOME_URL + p.find('a').get('href')
            img_src = p.find('img', class_='lazy').get('data-original')
            title = p.find('a').get('title')
            price_range = p.find('span', class_='price-range')
            if price_range.find('span', itemprop='lowPrice'):
                price = price_range.find('span', itemprop='lowPrice').get('content')
            else:
                price = price_range.text
                if '$' in price:
                    price = price.replace('$', '')
            new_result = Result(title)
            new_result.url = url
            new_result.image_src = img_src
            new_result.price = util.get_price(price)
            results.append(new_result)
            if len(results) == 10:
                return results
        except Exception as e:
            print("Error for product: ", p, e)

    return results


def main():
    print(extract_results('vacuum bump'))


if __name__ == '__main__':
    main()
