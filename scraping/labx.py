"""
@author Venita Boodhoo
Website: LabX
Status: Complete
Comment: For both new and used equipment
"""
import threading
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import util
from Result import Result
import requests

BASE_URL = "https://www.labx.com"
MAIN_URL = "https://www.labx.com/search?sw="
# MAIN_URL = "http://www.labx.com/v2/adsearch/search.cfm?sw="
DELIMITER = "+"


def extract_results(search_word: str, results: list, lock: threading.Lock, stop_event: threading.Event, condition='used'):
    # Url is extended based on condition
    if condition == "new":
        specific_url = util.create_url(MAIN_URL, search_word, DELIMITER) + "&condition=468_New"
    else:
        specific_url = util.create_url(MAIN_URL, search_word,
                                       DELIMITER) + "&condition=467_Used%2C469_Refurbished"
    # Check if page has data
    try:
        soup = util.get_soup(specific_url)
        table = soup.find('div', class_='grid-right-results')
        rows = table.find_all('a')
    except Exception as e:
        print(f"Error scraping {specific_url}: {e}")
        return

    # Get 1st 10 results only
    for row in rows:
        if stop_event.is_set():
            break
        try:
            title = row.find('div', class_="card-text-name").text.strip()
            url = row.get('href')
            url = BASE_URL + url
            img_src = row.find('img').get('src')
            price = row.find('div', class_="card-text-price")
            if not price:
                continue
            price = util.get_price(price.text.strip())
            if not util.is_valid_price(price):
                continue
            res = Result(title, url, price, img_src)
            lock.acquire()
            results.append(res)
            lock.release()
            if len(results) >= util.MAX_RESULTS:
                stop_event.set()
                break
        except Exception as e:
            print(f"Error scraping {row}: {e}")
    return


def main():
    lock = threading.Lock()
    stop_event = threading.Event()
    results = []
    extract_results('vacuum', results, lock, stop_event, 'used')
    print(results)


if __name__ == "__main__":
    main()
