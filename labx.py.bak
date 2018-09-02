"""
@author Venita Boodhoo
Website: LabX
Status: Complete
Comment: For both new and used equipment
"""

import urllib2
from bs4 import BeautifulSoup
import util 
from Result import Result
import requests

MAIN_URL = "https://www.labx.com/search?sw="
#MAIN_URL = "http://www.labx.com/v2/adsearch/search.cfm?sw="
DELIMITER = "+"

def extract_results(item,condition=None):
        #Url is extended based on condition
        if condition == "new":
                specific_url = util.create_url(MAIN_URL,item,DELIMITER) + "&condition=New,New%20or%20Used&adtype=998"
        else:
                specific_url = util.create_url(MAIN_URL,item,DELIMITER) + "&condition=Used,Refurbished,For%20Parts/Not%20Working,New%20or%20Used&adtype=998"     
        url = util.create_url(MAIN_URL,item, DELIMITER)
        results=[]
        #Check if page has data
        try:
            soup = util.check_exceptions(url)
            table = soup.find('tbody', class_='ResultsNewTable')
            rows=table.find_all('tr')
        except:
                  return []
        #Get 1st 10 results only
        for i in range(len(rows)):
                  row= rows[i]
                  new_result = Result(row.find('a').get('title'))
                  new_result.url = row.find('a').get('href')
                  new_result.price = util.get_price(row.find_all('td')[4].contents[0])
                  number = util.get_price(new_result.title)
                  new_result.image_src = "https://photos.labx.com/labx/"+number+"/"+number+"-0.jpg"
                  if util.is_valid_price(new_result.price):
                          results.append(new_result)
                          if len(results) == 10:
                                  return results
        return results

def main():
    print extract_results("vacuum pump", "new")

if __name__ == "__main__": main()
