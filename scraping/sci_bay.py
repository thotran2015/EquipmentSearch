"""
This website only contains used equipment
"""
import threading

import util
from bs4 import BeautifulSoup
from Result import Result

MAIN_URL = "http://www.sci-bay.com/?s="
DELIMITER = '+'


def extract_results(search_word: str, results: list, lock: threading.Lock, stop_event: threading.Event,
                    condition: str = 'used'):
    if condition == 'new':
        return []
    url = util.create_url(MAIN_URL, search_word, DELIMITER)
    soup = util.get_soup(url)
    table = soup.find('div', class_='content-area')
    rows = table.findAll("article")

    for row in rows:
        if stop_event.is_set():
            break
        title = row.find('h1', class_="entry-title").find("a").text
        result_url = row.find('a').get('href')
        # scrape from the result's page
        result_soup = util.get_soup(result_url)
        price = result_soup.find('span', class_="amount").text
        price = util.get_price(price)
        if not util.is_valid_price(price):
            continue
        img_src = result_soup.find('div', class_='images').find('img').get('src')
        res = Result(title, result_url, price, img_src)
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
    extract_results('centrifuge', results, lock, stop_event)
    print(results)


if __name__ == "__main__":
    main()
