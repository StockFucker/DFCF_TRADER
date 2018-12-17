
# -*- coding: utf-8 -*-

import sys
import os
import pandas as pd
import time
import json
import datetime
from trade import *
from flask import *

app = Flask(__name__)
trader=DFCF_Trader()

@app.route("/login")
def relogin():
    global trader
    trader=DFCF_Trader()
    login()
    return ""

@app.route("/buy")
def buy():
    print('buy: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') )
    stockcode = request.args.get('stockcode', '')
    stockname = ''
    price = request.args.get('price', '')
    amount = request.args.get('amount', '')
    tradetype = "B"
    if amount is None or amount == "" or int(amount) <= 0:
        trader.deal(stockcode,stockname,price,1.0,tradetype)
    else:
        trader.deal_with(stockcode,stockname,price,amount,tradetype)
    return ""

@app.route("/sell")
def sell():
    print('sell: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') )
    stockcode = request.args.get('stockcode', '')
    stockname = ''
    price = request.args.get('price', '')
    amount = request.args.get('amount', '')
    tradetype = "S"
    if amount is None or amount == "" or int(amount) <= 0:
        trader.deal(stockcode,stockname,price,1.0,tradetype)
    else:
        trader.deal_with(stockcode,stockname,price,amount,tradetype)
    return ""

@app.route("/asset")
def asset():
    return json.dumps(trader.getassets())

@app.route("/holdings")
def holdings():
    return json.dumps(trader.getstocklist())

@app.route("/hisorder")
def hisorder():
    st = request.args.get('begin', '')
    et = request.args.get('end', '')
    return json.dumps(trader.gethisorder(st,et))

@app.route("/hisdeal")
def hisdeal():
    st = request.args.get('begin', '')
    et = request.args.get('end', '')
    return json.dumps(trader.gethisdealdata(st,et))

def login():
    stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr  # 获取标准输入、标准输出和标准错误输出
    reload(sys)
    sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde  # 保持标准输入、标准输出和标准错误输出
    sys.setdefaultencoding('utf8')

    while True:
        if trader.login_flag==True:
            print "\nActive Threads: [%02d] \n" % threading.active_count()
            for i in xrange(threading.active_count()):
                print threading.enumerate()[i]
            print ''
            assets=trader.getassets()
            if assets:
                assets.update(trader.login_message['Data'][0])
                sys.stdout.write( "\r%(khmc)s <%(Syspm1)s>\tLogged at: %(Date)s-%(Time)s \
                                    **************************************************** \
                                   总资产:%(Zzc)s\t可用资金:%(Kyzj)s\t可取资金:%(Kqzj)s\t \
                                   冻结资金:%(Djzj)s\t    资金余额:%(Zjye)s   总市值: %(Zxsz)s " % assets)
                sys.stdout.flush()
            df=pd.DataFrame(trader.login_message['Data'])
            df=df.ix[:,[0,5,1,6]]
            df.columns = ['Date', 'Time','Account','Name']
            #print user.login_message['Data']
            #sys.stdout.write( "\r %(khmc)s <%(Syspm1)s> Logged at: %(Date)s-%(Time)s "  \
            #                  % user.login_message['Data'][0])

            break
        time.sleep(1)


if __name__ == '__main__':
    login()
    app.run()
