"""
@author Venita Boodhoo
Website: SibGene
Status: Complete
Comment: This website contains used and new equipment
"""

import urllib2
from bs4 import BeautifulSoup
import util
from Result import Result
import requests

MAIN_URL = "http://sibgene.com/index.php/catalogsearch/result/?q="
DELIMITER = "+"

def extract_results(item,requested_condition=None):
        url = util.create_url(MAIN_URL,item,DELIMITER)
        r = requests.get(url, timeout =3)
#        page = urllib2.urlopen(create_url(MAIN_URL,item,DELIMITER))
        soup = BeautifulSoup(r.content,"html.parser" )
        results=[]
        #Check for data
        try:
                table = soup.find_all('li',class_='item')
        except:
                return results
        #Get 1st 10 results only
        for i in range(len(table)):
                row=table[i]
                new_result = Result(row.find('a').get('title'))
                new_result.url = row.find('a').get('href')
                new_result.price = util.get_price(str(row.find('span',class_='price').find(text=True))\
                                   .encode('utf-8')[1:])
                new_result.image_src = row.find('img').get('src')
                
                specific_page = urllib2.urlopen(new_result.url)
                new_soup = BeautifulSoup(specific_page,"html.parser")
                condition = new_soup.find('div',class_='product-collateral').find('div',class_='std').text
                conditions = ['new','New','used','Used']
                bad_condition_types = ['bad','poor','not working','broken','not functional']
                #Check for matching conditions
                for word in conditions:
                        if word in condition:
                                if (requested_condition == None and word.lower() == 'used') or \
                                        (requested_condition != None and requested_condition.lower()== word.lower()):
                                        #Only add working good equipment
                                        for type_word in bad_condition_types:
                                                if type_word not in condition and util.is_valid_price(new_result.price):
                                                        results.append(new_result)
                                                        if len(results) == 10:
                                                                return results
        return results

def main():
    print extract_results("pump", "new")
    
if __name__ == "__main__": main()
