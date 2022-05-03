from datetime import datetime
from dotenv import load_dotenv
import os
import json
import pandas as pd
import plotly.graph_objects as go
import requests
import time
from client import FtxClient

load_dotenv()

global base
global data


def market():
    endpoint_url = 'https://ftx.com/api/markets'
    # Get all market data as JSON
    all_markets = requests.get(endpoint_url).json()
    # data manipulation
    df = pd.DataFrame(all_markets['result'])
    df.set_index('name', inplace=True)
    df = df.loc[df['type'] == 'spot']
    df = df.filter(['name', 'baseCurrency', 'quoteCurrency', 'bid'])

    return df


def usd():
    main = data
    usd = main.loc[main['quoteCurrency'] == 'USD']
    return usd


def base(cur):
    main = data
    base_ = main.loc[main['quoteCurrency'] == cur]
    return base_


crypto = 'USDT'
data = market()
usd_d = usd()
base = base(crypto)
base_bid_list = base['bid'].tolist()
name_list = base['baseCurrency'].tolist()

usdt_assets = 100
usd = 0
usd_list = []
global name_assets

for i in name_list:
    bid = base_bid_list[name_list.index(i)]

    name_assets = usdt_assets/bid

    usd_bid = usd_d.loc[usd_d['baseCurrency'] == i]
    usd_bid = usd_bid.filter(['bid'])
    usd_value = float(usd_bid['bid'])

    usd = float(name_assets*usd_value)
    print(usd)
    usd_list.append(usd)

    '''
    # alternate method
    bid = base.loc[base['baseCurrency'] == i]
    bid = bid.filter(['bid'])
    bid_value = float(bid['bid'])
    print(bid_value) 
    '''
print("-------------------------------")
large = max(usd_list)
print(large)