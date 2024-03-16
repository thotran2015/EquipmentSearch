"""
This website only contains used equipment
"""

import util
from bs4 import BeautifulSoup
from Result import Result

MAIN_URL = "http://www.sci-bay.com/?s="
DELIMITER = '+'


def extract_results(search_term, condition=None):
    if condition == 'new':
        return []
    url = util.create_url(MAIN_URL, search_term, DELIMITER)
    soup = util.get_soup(url)
    table = soup.find('div', class_='content-area')
    rows = table.findAll("article")

    results = []
    for row in rows:
        title = row.find('h1', class_="entry-title").find("a").text
        result_url = row.find('a').get('href')
        # scrape from the result's page
        result_soup = util.get_soup(result_url)
        price = result_soup.find('span', class_="amount").text
        price = util.get_price(price)
        img_src = result_soup.find('div', class_='images').find('img').get('src')
        new_result = Result(title, result_url, price, img_src)
        if util.is_valid_price(new_result.price):
            results.append(new_result)
            if len(results) == 10:
                return results
    return results


def main():
    results = extract_results("Beckman")
    # Printing the results the usual way gives an error because some elements contain u'2013
    try:
        print(results)
    except Exception as e:
        print(f"Error extracting {MAIN_URL}: {e}")


if __name__ == "__main__":
    main()
