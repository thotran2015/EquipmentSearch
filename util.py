import re
import string
import math
import requests
from bs4 import BeautifulSoup
from typing import Optional

MATCH_RATIO = .8

MAX_RESULTS = 10

MIN_RESULTS = 3


def get_price(price):
    """
    Takes in a string containing the price of the equipment and results the price only (decimal in a string)
    @param price a String of text containing the price of the equipment
    @return number a String containing only numbers and a decimal pt representing the price of the equipment
    """
    # price input is string
    allow = string.digits + '.,'
    number = re.sub('[^%s]' % allow, '', str(price))
    return number.strip()


def is_valid_price(price):
    """
    Takes in a string containing the price of the equipment
    @param price a String of text containing the price of the equipment
    @return True if the string price is the same when only a decimal and #s are kept else False
    """
    price = get_price(price)
    return bool(price)


def str_to_float(price):
    """
    Converts a string to float
    @param price a String of text containing the price of the equipment
    @return number a float representing the price of the equipment
    """
    price = price.replace('$', '')
    price = price.replace(',', '')
    return float(price)


def price_prettify(float_price):
    """
    Formats a float to have 2 decimal places and a dollar sign
    @param float_price a float representing the price of the equipment
    @return a float whose format is Sfloat_price.00  representing the price of the equipment
    """
    try:
        return "$" + '{:20,.2f}'.format(float_price).replace(' ', '')
    except:
        return "None"


def create_url(main_url, search_term, delimiter):
    """
    Formats a float to have 2 decimal places and a dollar sign
    @param main_url, a String containing the website search url
    @param search_term, a String describing the terms to search for
    @param delimiter, a single char indicating how the site searches multiple words e.g. '%20' or '+'
    @return specific_url, a String containing the main_url+search_words
    """
    specific_url = main_url
    search_words = search_term.split()
    for i in range(len(search_words)):
        if i != 0:
            specific_url = specific_url + delimiter + search_words[i]
        else:
            specific_url = specific_url + search_words[i]
    return specific_url


def get_soup(url, timeout=5) -> Optional[BeautifulSoup]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, timeout=timeout, headers=headers)
        if response.status_code == 200:
            return BeautifulSoup(response.content, "html.parser")
        else:
            print(f"Status code: {response.status_code}. Try again!")
    except requests.Timeout as e:
        print(f"This is timeout: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")
    except Exception as e:
        print(f"Error getting soup for {url}: {e}")


def sort_by_price(results):
    """
    sorts a list of Results by price
    @param results, a list of Result obects
    @return results, a list of Results sorted by price
    """
    results.sort(key=lambda x: str_to_float(x.price), reverse=True)
    return results


def median_price(results):
    """
    Finds of the median price of any sized list of Results.
    If an even length list, returns the value closest to the avg in the middle.
    @param results, a List of Result objects
    @return price, a String, indicating the median price value
    """
    prices = []
    for equip in results:
        if equip.price is not None and equip.price != '':
            prices.append(str_to_float(equip.price))
    if not prices:
        return "None"
    avg = float(sum(prices)) / len(prices)
    prices.sort()
    length = len(prices)
    if length % 2 == 0:
        if abs(prices[(length - 1) // 2] - avg) <= abs(prices[(length + 1) // 2] - avg):
            return prices[(length - 1) // 2]
        return prices[(length + 1) // 2]
    # Odd length prices list
    return prices[(length - 1) // 2]


def is_close_match(search_term, result_term):
    """
    checks if the result contains at least MATCH_RATIO of the search words
    search_term, result_term are strings
    """
    search_words = search_term.split()
    match_number = 0
    for word in search_words:
        if word.lower().strip() in result_term.lower():
            match_number += 1
    return match_number >= math.ceil(len(search_words) * MATCH_RATIO)
