#!/usr/bin/env python
# -*- coding: utf-8 -*-

from trade_calendar import TradeCalendar
import tushare as ts
import time

class StockPool(object):
    """
    利用历史数据选出自己的股票， 放入股票池
    
    返回数据为pandas格式
    """
    def __init__(self):
        self.stockIDs=None
        self.stock_pool=None
        self.calendar=TradeCalendar()        
        
    def generatge_basic_stockcode(self):
        df = ts.get_stock_basics()
        self.stockIDs=df.index
        
        df = ts.get_today_all()
        df[df['name'].str.contains('[ST]').values==False] #去掉股票代码包含ST的股票
        #df[(df['name'].str.contains('[ST]').values==False)&(df['trade']==0)] 
        
    def generate_stock(self):
        pass
        
    def get_hist_data(self,code,start,end):
        df = ts.get_hist_data(code=code,start=start,end=end,ktype='D',retry_count=3,pause=0.001)
        return df

    def is_break_high(self,stockID,days):  
        #end_day=datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day)  
        #end_day=end_day.strftime("%Y/%m/%d")  
        #end_day=time.strftime('%Y-%m-%d',time.localtime())
        #start_day=self.calendar.trade_calendar(end_day.replace('-','/'),days).replace('/','-')
        df=ts.get_hist_data(stockID,start=start_day,end=end_day)  
        if df is None: return False
        if len(df)==0 or df.empty or df.index[0] <> end_day:
            return False
        period_high=df['high'].max()  #区间最高价
        period_low=df['low'].min()
        ma5=round(df.ix[end_day].ma5,2)
        ma10=round(df.ix[end_day].ma10,2)
    
        #print period_high  
        today_high=df.iloc[0]['high']  
        #这里不能直接用 .values  
        #如果用的df【：1】 就需要用.values  
        #print today_high  
        if today_high>=period_high:  
            return True  
        else:  
            return False  
        
if __name__=="__main__":
    test=StockPool()
    stockID ,start,end='600000', '2017-05-10', '2017-05-18'
    df= test.get_hist_data(stockID,start,end)
    print df
    a= df.ix[0,['ma5']] #df.ix['2017-05-17',['ma5']]
    print a
    print type(a)
    print a[0]
    
    info=ts.get_stock_basics()  
    today=time.strftime('%Y-%m-%d',time.localtime())
    end_day=test.calendar.trade_calendar(today.replace('-','/'),-2).replace('/','-')
    start_day=test.calendar.trade_calendar(end_day.replace('-','/'),-10).replace('/','-')
    i=1;stocks={}
    print len(info)
    def loop_all_stocks():
        global i
        for EachStockID in info.index:  
             print i,EachStockID;i+=1
             if test.is_break_high(EachStockID,-10):  
                 print "High price on",  
                 print EachStockID,  
                 print info.ix[EachStockID]['name'].decode('utf-8')  
                 stocks[EachStockID]=info.ix[EachStockID]['name'].decode('utf-8')
    loop_all_stocks() 