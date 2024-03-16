"""
Created on Mon Jan  9 18:06:56 2017

@author: thotran
Marshall Scientific sells used equipment only. 
"""
import util
from Result import Result
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


MAIN_URL = "http://www.marshallscientific.com/searchresults.asp?Search="
DELIMITER = '+'


def extract_results(search_word, condition=None):
    if condition == "new":
        return []
    url = util.create_url(MAIN_URL, search_word, DELIMITER)
    try:
        soup = util.get_soup(url)
        product_grid = soup.find('div', class_='v-product-grid')
        if not product_grid:
            return []
        total_equips = product_grid.find_all('div', class_='v-product')
    except Exception as e:
        logging.exception(f"Can't soup at {url}: {e}")
        return []
    equips = []

    for equip in total_equips:
        title = equip.find('a', class_='v-product__title productnamecolor colors_productname').find(string=True).strip()
        equipment = Result(title)
        equipment.url = equip.find('a', class_='v-product__img').get('href')
        equipment.image_src = 'http:' + equip.find('img').get('src')
        price_text = equip.find('div', class_='product_productprice').find_all(string=True)
        equipment.price = util.get_price(''.join(price_text))
        if util.is_valid_price(equipment.price):
            equips.append(equipment)
        if len(equips) >= 10:
            return equips
    return equips


def main():
    print(extract_results('vacuum'))


if __name__ == '__main__':
    main()
