import re
import string
import numpy
import math
from Result import *
import requests
from bs4 import BeautifulSoup

'''
Takes in a string containing the price of the equipment and results the price only (decimal in a string)
@param price a String of text containing the price of the equipment
@return number a String containing only numbers and a decimal pt representing the price of the equipment
'''
def get_price(price):
    #price input is string
    allow = string.digits + '.,'
    number = re.sub('[^%s]' %allow,'',str(price))
    return number.strip()

'''
Takes in a string containing the price of the equipment
@param price a String of text containing the price of the equipment
@return True if the string price is the same when only a decimal and #s are kept else False
'''
def is_valid_price(price):
    price=get_price(price)
    return bool(price)

'''
Converts a string to float
@param price a String of text containing the price of the equipment
@return number a float representing the price of the equipment
'''
def str_to_float(price):
    price = price.replace('$','')
    price = price.replace(',','')
    return float(price)

'''
Formats a float to have 2 decimal places and a dollar sign
@param float_price a float representing the price of the equipment
@return a float whose format is Sfloat_price.00  representing the price of the equipment
'''
def price_prettify(float_price):
    try:
        return "$" +'{:20,.2f}'.format(float_price).replace(' ','')
    except:
        return "None"

'''
Formats a float to have 2 decimal places and a dollar sign
@param main_url, a String containing the website search url
@param search_term, a String describing the terms to search for
@param delimter, a single char indicating how the site searches multiple words e.g. '%20' or '+'
@return specific_url, a String containing the main_url+search_words
'''
def create_url(main_url, search_term, delimiter):
    specific_url=main_url
    search_words=search_term.split()
    for i in range(len(search_words)):
        if i!=0:
            specific_url= specific_url + delimiter+ search_words[i]
        else:
            specific_url= specific_url + search_words[i]
    return specific_url




def check_exceptions(url, timeout = 5, headers = None):
    try:
        response = requests.get(url, timeout = 5, header = None)
        if response.status_code == 200:
            return BeautifulSoup(response.content,"html.parser")
        else:
            print(("Status code: ", response.status_code))
            print("try again")
    except requests.Timeout as e:
        print("This is timeout")
        print((str(e)))
    except requests.exceptions.RequestException:
        print ("Error")
        
'''
sorts a list of Results by price
@param results, a list of Result obects
@return results, a list of Results sorted by price
'''
def sort_by_price(results):
    results.sort(key=lambda x: str_to_float(x.price), reverse=True)
    return results

'''
Finds of the median price of any sized list of Results.
If an even length list, returns the value closest to the avg in the middle.
@param results, a List of Result objects
@return price, a String, indicating the median price value
'''
def median_price(results):
    prices=[]
    for equip in results:
        if equip.price!=None and equip.price!='': 
            prices.append(str_to_float(equip.price))
    if prices == []:
        return "None"
    avg = float(sum(prices))/len(prices)
    prices.sort()
    length = len(prices)
    if length % 2 == 0:
        if abs(prices[(length-1)/2]-avg) <= abs(prices[(length+1)/2]-avg):
            return prices[(length-1)/2]
        return prices[(length+1)/2]
    #Odd length prices list
    return prices[(length-1)/2]
    
