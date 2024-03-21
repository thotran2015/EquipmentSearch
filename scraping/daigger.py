"""
@author Venita Boodhoo
Website: daigger
Status: Complete
Comments: For new equipment only
"""
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup

import util
from util import *
from Result import Result

MAIN_URL = "http://www.daigger.com/products-search?qs="
HOME_URL = "http://www.daigger.com"                    
DELIMITER = "+"

def extract_results(item,condition=None):
        results=[]
        if condition != "new":
                return results
        specific_url = create_url(MAIN_URL,item,DELIMITER)
        soup = util.get_soup(specific_url)

        table = soup.find('div',id ="ListingProducts")
        #Check for data
        try:
                  #If items are a list
                  rows=table.find_all('div',class_="boxshad productbox")
        except:
                  try:
                          #Returns one item on a specific pg
                          new_result = Result(soup.find('h1',itemprop='name'))
                          new_result.url = specific_url
                          new_result.image_src = HOME_URL+soup.find('div',class_='product-image').find('img').get('src')
                          items = soup.find_all('tr',class_='ejs-addtocart-section')
                          for item in items:
                                #Supplier #
                                supplier = item.find('span',class_='supplier-code')
                                if supplier != None:
                                        new_result.title = new_result.title + supplier.text
                                new_result.price = item.find('strong',class_='price').text
                                currency = item.find('span',itemprop='priceCurrency')
                                if (currency == None or currency.text == "USD") and is_valid_price(new_result.price):
                                        results.append(new_result)
                                        if len(results)==9:
                                                return results
                                #Reset title to original product name for next model of item
                                new_result.title = soup.find('h1',itemprop='name').text
                          
                          return results
                  #No results found
                  except:
                          return []
        
        #For multiple items  
        for row in table.find_all('div',class_="boxshad productbox"):
                new_result = Result(row.find('a').get('title'))
                new_result.url = HOME_URL + row.find('a').get('href')
                new_result.image_src = HOME_URL + row.find('img').get('src')
                specific_page = urllib.request.urlopen(new_result.url)
                new_soup = BeautifulSoup(specific_page,"html.parser")
                #Get all models of products from specific page
                items = new_soup.find_all('tr',class_='ejs-addtocart-section')
                for item in items:
                        #Supplier Number
                        supplier = item.find('span',class_='supplier-code')
                        if supplier != None:
                                new_result.title = new_result.title + supplier.text
                        new_result.price = item.find('strong',class_='price').text
                        currency = item.find('span',itemprop='priceCurrency')
                        
                        if (currency == None or currency.text == "USD") and is_valid_price(new_result.price):
                                results.append(new_result)
                                if len(results) == 9:
                                        return results
                        #Reset title to original product name for next model of item
                        new_result.title = row.find('a').get('title')
                
        return results

def main():
    print(extract_results("vacumm pump","new"))

if __name__ == "__main__": main()
