import sys
import os  
import pandas as pd
import time
import json
import urllib

dates = ["2018-01-01","2018-05-05"]

def get_deals():
    dfs = []
    for i in range(len(dates) - 1):
        begin = dates[i]
        end = dates[i+1]
        url = "http://localhost:5000/hisdeal?begin=" + begin + "&end=" + end
        data=urllib.urlopen(url).read()
        df = pd.DataFrame(json.loads(data.decode()))
        dfs.append(df)
    data_df = pd.concat(dfs)
    data_df = data_df[data_df["Cjje"].astype(float) > 8000]
    data_df = data_df.sort(["Jsrq"])
    data_df = data_df.set_index(["Zqdm","Wtsl"],inplace=False)
    buy_df = data_df[data_df["Mmlb"] == "B"]
    sell_df = data_df[data_df["Mmlb"] == "S"]
    buy_df = buy_df[~buy_df["Cjje"].duplicated()]
    sell_df = sell_df[~sell_df["Cjje"].duplicated()]
    sep_sell = set(sell_df.index) - set(buy_df.index)
    sep_sell_df = sell_df.ix[sep_sell]
    sep_sell_df = sep_sell_df.reset_index()
    sep_sell_df["Wtsl"] = sep_sell_df["Wtsl"].astype(int)
    cjsl_se = sep_sell_df.groupby(["Zqdm"]).sum()["Wtsl"]
    sep_sell_df = sep_sell_df.groupby(["Zqdm"]).first()
    sep_sell_df["Wtsl"] = cjsl_se
    sep_sell_df = sep_sell_df.reset_index()
    sep_sell_df["Wtsl"] = sep_sell_df["Wtsl"].astype(str)
    sep_sell_df = sep_sell_df.set_index(["Zqdm","Wtsl"],inplace=False)
    sell_df = sell_df.append(sep_sell_df)
    sell_df = sell_df.ix[buy_df.index]
    buy_df = buy_df.ix[sell_df.index]

    buy_df["sell_price"] = sell_df["Cjjg"]
    buy_df["buy_price"] = buy_df["Cjjg"]
    buy_df["sell_time"] = sell_df["Cjsj"]
    return buy_df

def get_orders():
    dfs = []
    for i in range(len(dates) - 1):
        begin = dates[i]
        end = dates[i+1]
        url = "http://localhost:5000/hisorder?begin=" + begin + "&end=" + end
        data=urllib.urlopen(url).read()
        df = pd.DataFrame(json.loads(data.decode()))
        dfs.append(df)
    data_df = pd.concat(dfs)
    data_df["Wtje"] = data_df["Wtjg"].astype(float) * data_df["Wtsl"].astype(float)
    data_df = data_df[data_df["Wtje"]> 5000]
    data_df = data_df[data_df["Mmlb"] != "Q"]
    data_df = data_df[data_df["Mmlb"] != "P"]
    data_df = data_df.sort(["Wtrq"])
    data_df = data_df.set_index(["Zqdm","Wtsl"],inplace=False)
    buy_df = data_df[data_df["Mmlb"] == "B"]
    sell_df = data_df[data_df["Mmlb"] == "S"]
    buy_df = buy_df[~buy_df["Wtje"].duplicated()]
    sell_df = sell_df[~sell_df["Wtje"].duplicated()]
    sep_sell = set(sell_df.index) - set(buy_df.index)
    sep_sell_df = sell_df.ix[sep_sell]
    sep_sell_df = sep_sell_df.reset_index()
    sep_sell_df["Wtsl"] = sep_sell_df["Wtsl"].astype(int)
    cjsl_se = sep_sell_df.groupby(["Zqdm"]).sum()["Wtsl"]
    sep_sell_df = sep_sell_df.groupby(["Zqdm"]).first()
    sep_sell_df["Wtsl"] = cjsl_se
    sep_sell_df = sep_sell_df.reset_index()
    sep_sell_df["Wtsl"] = sep_sell_df["Wtsl"].astype(str)
    sep_sell_df = sep_sell_df.set_index(["Zqdm","Wtsl"],inplace=False)
    sell_df = sell_df.append(sep_sell_df)
    sell_df = sell_df.ix[buy_df.index]
    sell_df = sell_df[~sell_df.index.duplicated()]
    buy_df["sell_price"] = sell_df["Wtjg"]
    buy_df["buy_price"] = buy_df["Wtjg"]
    buy_df["sell_time"] = sell_df["Wtsj"]
    return buy_df

def go():
    # deal_df = get_deals()
    order_df = get_orders()

if __name__ == '__main__':
    go()