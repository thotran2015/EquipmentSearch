"""
This website sells used equipment
"""
import threading

import util
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
from Result import Result

HOME_URL = "http://www.equipnet.com"
MAIN_URL = "http://www.equipnet.com/search/?q="
DELIMITER = "%20"


def extract_results(search_word: str, results: list, lock: threading.Lock, stop_event: threading.Event,
                    condition: str = None):
    if condition == 'new':
        return
    url = util.create_url(MAIN_URL, search_word, DELIMITER)
    soup = util.get_soup(url)
    table = soup.find('div', class_="search-results-container")
    rows = table.findAll("div", class_="row")
    for row in rows:
        if stop_event.is_set():
            break
        # Extract title
        title_tag = row.find('h6', class_='title listing-title-padding')
        if title_tag is None:
            continue
        title = title_tag.text.strip()
        if not util.is_close_match(search_word, title):
            continue
        # Extract price
        price_tag = row.find('span', class_='price-amount')
        price = price_tag.text.strip() if price_tag else None
        price = util.get_price(price)
        if not util.is_valid_price(price):
            continue
        # Extract URL
        url_tag = row.find('a', href=True)
        url = url_tag['href'] if url_tag else None
        if url and 'http' not in url:
            url = HOME_URL + url
        # Extract image URL
        image_tag = row.find('img', class_='list-view-thumbnail')
        image_url = image_tag['src'] if image_tag else None
        res = Result(title, url, price, image_url)
        lock.acquire()
        results.append(res)
        lock.release()
        if len(results) >= util.MAX_RESULTS:
            stop_event.set()
            break
    return


def main():
    lock = threading.Lock()
    stop_event = threading.Event()
    results = []
    extract_results("Beckman Coulter Biomek Workstation", results, lock, stop_event)
    print("result 1: ", results)
    extract_results("Workstation", results, lock, stop_event)
    print("result 2: ", results)


if __name__ == "__main__":
    main()
