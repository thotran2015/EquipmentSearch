"""
@author Venita Boodhoo
Website: LabCommerce
Status: Complete
Note: Sells used products only
"""

import urllib2
from bs4 import BeautifulSoup
from util import *
from Result import Result


MAIN_URL = 'http://www.labcommerce.com'
SEARCH_URL = "http://www.labcommerce.com/searchresults.php?txtsearch="
DELIMITER = "+"

def extract_results(item,condition=None):
        results=[]
        if condition != 'new':
                page = urllib2.urlopen(create_url(SEARCH_URL,item,DELIMITER)+"&image.x=0&image.y=0")
                soup = BeautifulSoup(page,"html.parser")
                table = soup.find_all('div',class_="search_result")
                
                for row in table:
                        #.encode('utf-8') is used because to convert text to str since
                        #not all of the characters are recognized
                        new_result = Result(row.a.text.encode('utf-8').strip())
                        url = re.sub('/catid/','.php?catid=',row.find('a').get('href'))
                        #Omit last slash
                        specific_url = re.sub('/prodid/','&prodid=',url)[:-1]
                        new_result.url = MAIN_URL+ specific_url.encode('utf-8').strip()
                        new_soup = BeautifulSoup(urllib2.urlopen(new_result.url),"html.parser")
                        #Omit surrounding text, get decimal only
                        new_result.price = get_price(str(new_soup.find('td',class_='price').find_all(text=True)[0])\
                                           .encode('utf-8').strip())
                        #Omit 1st char (a period)
                        new_result.image_src = MAIN_URL+new_soup.find('td',align='center')\
                                               .find('img').get('src')[1:].encode('utf-8').strip()
                        
                        bad_condition_types = ['bad','poor','not working','broken','not functional']
                        condition_type_text = new_soup.find(text='Condition:')
                        #Matches on condition and omits bad conditions
                        if condition_type_text != None:
                                condition_type = condition_type_text.find_next(text=True)
                                for word in bad_condition_types:
                                        if word not in condition_type and is_valid_price(new_result.price):
                                                results.append(new_result)
                        elif is_valid_price(new_result.price):
                                results.append(new_result)
        
        return results

def main():
    print extract_results("pump")

if __name__ == "__main__": main()
