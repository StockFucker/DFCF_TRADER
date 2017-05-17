#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tushare as ts

class StockPool(object):
    """
    利用历史数据选出自己的股票， 放入股票池
    
    返回数据为pandas格式
    """
    def __init__(self):
        self.stock_pool=[]
        
    def generate_stock(self):
        pass
        
    def get_hist_data(self,code,start,end):
        df = ts.get_hist_data(code=code,start=start,end=end,ktype='D',retry_count=3,pause=0.001)
        return df
    
if __name__=="__main__":
    test=StockPool()
    code ,start,end='600000', '2017-05-10', '2017-05-18'
    df= test.get_hist_data(code,start,end)
    print df
    a= df.ix[0,['ma5']] #df.ix['2017-05-17',['ma5']]
    print a
    print type(a)
    print a[0]