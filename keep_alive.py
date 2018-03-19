#!/usr/bin/python3
# -*- coding: utf-8 -*-
# return all stocks information include price and voloum, excluding ST and risk notification stocks

import json

import requests  
import time

def go():
    LOGIN_URL = "http://localhost:5000/asset"
    data=requests.get(LOGIN_URL)
    # LOGIN_URL = "http://localhost:7000/asset"
    # data=requests.get(LOGIN_URL)

if __name__ == '__main__':
    while True:
        time.sleep(60)
        go()