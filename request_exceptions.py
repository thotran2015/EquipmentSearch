#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 07:36:05 2018

@author: thotran
"""
import requests

def check_exceptions(url):
    try:
        response = requests.get(url, timeout = 5)
        if response.status_code == 200:
            return response
        else:
            print(("Status code: ", response.status_code))
            print("try again")
    except requests.Timeout as e:
        print("This is timeout")
        print((str(e)))