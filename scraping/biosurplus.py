"""
This website sells pre-owned equipment
"""
import gzip
import io
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

import util
from Result import Result

MAIN_URL = "http://www.biosurplus.com/store/search/?per_page=24&product_search_q="
DELIMITER = '+'


def extract_results(search_term, condition=None):
    if condition == 'new':
        return []
    headers = {
        'Host': 'www.biosurplus.com',
        'Connection': 'keep-alive',
        'Accept': 'text/html',
        'Referer': 'http://www.biosurplus.com/store/search/?per_page=24&product_search_q=Beckman+Coulter+Biomek+Workstation',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
    url = util.create_url(MAIN_URL, search_term, DELIMITER)
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req)

    # This page is g-zipped. Unzip it
    stringified_data = io.StringIO(page.read())
    unzipped_page = gzip.GzipFile(fileobj=stringified_data)

    soup = BeautifulSoup(unzipped_page, "html.parser")
    table = soup.find('div', class_='product_browse')
    try:
        # check if the table
        rows = table.findAll("div", class_="fps_featured_product")
    except:
        return []
    results = []
    for row in rows:
        manufacturer = row.find('p', class_="fps_fp_description").find(text=True)
        title = row.find('h2', class_="fps_fp_heading").find("a").find(text=True)
        new_result = Result(manufacturer + " " + title)
        new_result.price = util.get_price(row.find('p', class_='product_price').find(text=True))
        new_result.image_src = row.find('div', class_="fps_fp_image_inner").find('img').get('src')
        new_result.url = "www.biosurplus.com" + row.find('a').get('href')
        if util.is_valid_price(new_result.price):
            results.append(new_result)
            if len(results) == 10: return results
    return results


def main():
    print(extract_results("Beckman Coulter Biomek Workstation"))


if __name__ == "__main__":
    main()
