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
                
    def generate_stockpool(self):
        info =  ts.get_today_all() # ts.get_stock_basics()
        self.stock_pool = info[(info['name'].str.contains('[ST]').values==False) & (info['open'] <> 0)]  #去除掉 ST & 未交易
        
    def get_hist_data(self,code,start,end):
        df = ts.get_hist_data(code=code,start=start,end=end,ktype='D',retry_count=3,pause=0.001)
        return df

    #判断是否窗新高
    def is_break_high(self,stockID,days):  
        #end_day=datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day)  
        #end_day=end_day.strftime("%Y/%m/%d")  
        #end_day=time.strftime('%Y-%m-%d',time.localtime())
        #start_day=self.calendar.trade_calendar(end_day.replace('-','/'),days).replace('/','-')
        df=ts.get_hist_data(stockID,start=start_day,end=end_day)  
        if df is None: return False
        if len(df)==0 or df.index[0] <> end_day:
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
    
    #判断是否涨停    
    def is_top_price(self,stockID,before=1):
        df=ts.get_k_data(stockID)[::-1]
        if len(df)>15 and df.iloc[0].date == end_day:
            if round(df.iloc[before-1].close,2) == round(round(df.iloc[before].close,2)*1.1, 2):
                buy_value = self.get_buy_value(df,before)
                return True,buy_value
            else:
                return False
        else:
            return False
    
    #获取均线数值    
    def get_ma(self,stockID,ma=5):
        sum=0
        df=ts.get_k_data(stockID)[::-1]
        if df.empty:
            return 0
        elif len(df)<ma:
            ma=len(df)
        for _ in xrange(ma):
            sum+=round(df.iloc[_].close,2)
        return round(sum/ma,2)
    
    #获取买入价格 涨停价格后两天内距离最高点 下跌 7%
    def get_buy_value(self,df,before,fall=7):
        print df
        print round(df.iloc[0:before]['high'].max()*(100-fall)/100.0, 2)
        return round(df.iloc[0:before]['high'].max()*(100-fall)/100.0, 2)

if __name__=="__main__":
    test=StockPool()
    test.generate_stockpool()
    info=test.stock_pool

    today=time.strftime('%Y-%m-%d',time.localtime())
    end_day=test.calendar.trade_calendar(today.replace('-','/'),-2).replace('/','-')
    start_day=test.calendar.trade_calendar(end_day.replace('-','/'),-10).replace('/','-')
    
    i=1;stocks={}
    print len(info)
    
    def loop_all_stocks():
        global i
        for EachStockID in info.code: # info.index:  
             print i,EachStockID;i+=1
             #if test.is_break_high(EachStockID,-10):
             result= test.is_top_price(EachStockID,2)
             if result:
                 print "High price on",
                 print EachStockID,  
                 print info[info.code==EachStockID].name.values[0]  #info.ix[EachStockID]['name'].decode('utf-8')  
                 stocks[EachStockID] = info[info.code==EachStockID].name.values[0],test.get_ma(EachStockID),result[1] #info.ix[EachStockID]['name'].decode('utf-8')
    loop_all_stocks() 
    
    for _ in stocks:
        print _,stocks[_]
        