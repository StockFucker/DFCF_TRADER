#!/usr/bin/python3
# -*- coding: utf-8 -*-
# return all stocks information include price and voloum, excluding ST and risk notification stocks

import json
# from download import download
import pandas as pd
import easyquotation
import re
import urllib
from datetime import datetime, timedelta
from tradeday import *
from constant import *
from valid_quotes import *
import time
from ml import *


BEGIN_TIME = '09:30:00'
ml = ML()

def go():
    LOGIN_URL = "http://localhost:5000/asset"
    data=urllib.request.urlopen(LOGIN_URL).read()
    LOGIN_URL = "http://localhost:7000/asset"
    data=urllib.request.urlopen(LOGIN_URL).read()

if __name__ == '__main__':
    while True:
        sleep(60)
        go()