# -*- coding: utf-8 -*-

from __future__ import division
import re
import time,sys
import requests
import threading
import winsound
import pandas as pd
import tushare


class PriceQuotation(object):
    def __init__(self,stockcode='600000'):
        self.kill=0
        self.show=0
        self.stockcode=False
        self.result=False
        self.thread_2 = threading.Thread(target=self.get_tushare_quote,name='Thread__Monitor__Price')
        self.thread_2.setDaemon(True)
        self.thread_2.start()

    #获取实时行情
    def get_tushare_quote(self):
        while True:
            if self.kill==1:
                winsound.PlaySound('./wav/stop price monitor CN.wav',winsound.SND_ASYNC)
                break
            if self.stockcode <> False:
                self.result=tushare.get_realtime_quotes(self.stockcode)
                self.show_tushare_price(self.result)
            time.sleep(0.1)
    def show_tushare_price(self, quote):
        if self.show==1:
            sys.stdout.write("\r    *%s %s: %.2f  %.2f%%" % \
                         (time.strftime("%Y-%m-%d %X"),\
                          quote['name'][0],\
                          float(quote['price'][0]),\
                          (float(quote['price'][0])-float(quote['pre_close'][0]))/float(quote['pre_close'][0])*100))    
 
    
 #-------------------------------华丽的分割线-------------------  
    def get_quote(self):
        self.s = requests.session()
        while True:
            if self.kill==1:
                winsound.PlaySound('./wav/stop price monitor CN.wav',winsound.SND_ASYNC)
                break
            if self.stockcode <> False:
                params={
                        'id':self.stockcode,
                        'callback':'',#'jQuery18302588442438663068_1484803703313',
                        '_':'' # repr(time.time()).replace(".","")
                       }
                try:
                    quote=self.s.get('https://hsmarket.eastmoney.com/api/SHSZQuoteSnapshot',params = params)
                    
                except Exception:
                    #log.error('price quotation error!');time.sleep(1)
                    print 'price quotation error!';time.sleep(1)
                    continue
                self.result=eval(re.search(r'{.*}',quote.text).group())
                self.show_price(self.result)
            time.sleep(1)      
    def show_price(self, quote):
        if self.show==1:
            sys.stdout.write("\r    *%s %s: %s  %s" % \
                         (time.strftime("%Y-%m-%d %X"),\
                          quote['name'],\
                          quote['realtimequote']['currentPrice'],\
                          quote['realtimequote']['zdf']))
            

    def get_hist_price(self,stockcode='000001.ss',s_date='2017-01-01',e_date=time.strftime('%Y-%m-%d',time.localtime())):
        '''
        深市数据链接：http://table.finance.yahoo.com/table.csv?s=000001.sz
        上市数据链接：http://table.finance.yahoo.com/table.csv?s=600000.ss
        上证综指代码：000001.ss
        '''
        if stockcode.startswith(('6')) and not stockcode.endswith(('ss')):
            stockcode+='.ss'
        elif stockcode.startswith(('0','2','3')) and not stockcode.endswith(('ss')):
            stockcode+='.sz'
        else:
            stockcode=stockcode

        a,b,c=str(int(s_date[5:7])-1),s_date[8:10],s_date[0:4]
        d,e,f=str(int(e_date[5:7])-1),e_date[8:10],e_date[0:4]
        url='http://table.finance.yahoo.com/table.csv?s='+stockcode
        url+='&d='+d+'&e='+e+'&f='+f+'&g=d&a='+a+'&b='+b+'&c='+c+'&ignore=.csv' #注意：月份要比实际月份少 1 
        df= pd.read_csv(url)
        return df
# ------------------------------------------------------------------



    def get_hist_data(self,code='600898',s_date='2017-01-01',e_date=time.strftime('%Y-%m-%d',time.localtime())):
        stockcode=code
        start=s_date
        end=e_date
        return tushare.get_k_data(stockcode,start,end)

if __name__=="__main__":
    '''
    df=PriceQuotation().get_hist_price('600898','2017-02-01')
    index=df[df['Date']=='2017-02-10'].index[0]
    Open,High,Low=df.ix[index,'Open'],df.ix[index,'High'],df.ix[index,'Low']
    show_list=[]
    show_list.append(Open);show_list.append(High);show_list.append(Low)
    
    print df
    print index,show_list
    '''
    test=PriceQuotation()
    df=test.get_hist_data('600300','2017-02-01')
    index=df[df['date']=='2017-02-10'].index[0]
    Open,High,Low=df.ix[index,'open'],df.ix[index,'high'],df.ix[index,'low']
    show_list=[]
    show_list.append(Open);show_list.append(High);show_list.append(Low)
    print df
    print show_list
    print '{0:.2f}'.format(show_list[1])
    print format(show_list[1], '.2f')
    test.stockcode='600898'
    test.show=1