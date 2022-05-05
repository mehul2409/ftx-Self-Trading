from datetime import datetime
from dotenv import load_dotenv
import os
import json
import pandas as pd
import plotly.graph_objects as go
import requests
import time
from client import FtxClient
from mail import send

load_dotenv()
ftx_client = FtxClient(
    api_key=os.getenv("FTX_API_KEY"),
    api_secret=os.getenv("FTX_API_SECRET")
)

global base
global data


def market():
    try:

        endpoint_url = 'https://ftx.com/api/markets'
        # Get all market data as JSON
        all_markets = requests.get(endpoint_url).json()
        # data manipulation
        df = pd.DataFrame(all_markets['result'])
        df.set_index('name', inplace=True)
        df = df.loc[df['type'] == 'spot']
        df = df.filter(['name', 'baseCurrency', 'quoteCurrency', 'bid'])

        return df
    except Exception as e:
        send(e)
        print(f'Error making order request: {e}')
        os.system.exit()


def usd():
    main = data
    usd = main.loc[main['quoteCurrency'] == 'USD']
    return usd


def base(cur):
    main = data
    base_ = main.loc[main['quoteCurrency'] == cur]
    return base_


def wall(cur):
    bal = ftx_client.get_all_balances()
    usdtbal1 = bal['main']
    for i in range(len(usdtbal1)):
        usdtbal2 = usdtbal1[i]
        if (usdtbal2['coin'] == cur):
            usdtbal3 = usdtbal2['total']
            break
        else:
            usdtbal3 = 'usd not found'
    return usdtbal3


def placeoder(name, large, calculate, action):
    try:
        bo_result = ftx_client.place_order(
            market=f"{name}",
            side=action,
            type='market',
            price=large,
            size=calculate
        )
        print(bo_result)
    except Exception as e:
        send('The process sto while performing transuction on ' + name)
        print(f'Error making order request: {e}')
        os.system.exit()


x = 1
# Looping proces starts here
while x == 1:

    x = 0
    crypto = 'USDT'
    data = market()
    usd_d = usd()
    base = base(crypto)
    base_bid_list = base['bid'].tolist()
    name_list = base['baseCurrency'].tolist()

    usdtbal = wall('USDT')
    usdt_assets = usdtbal - 1
    usd = 0
    usd_list = []
    global name_assets
    bid_list = []

    for i in name_list:
        bid = base_bid_list[name_list.index(i)]

        name_assets = usdt_assets / bid

        usd_bid = usd_d.loc[usd_d['baseCurrency'] == i]
        usd_bid = usd_bid.filter(['bid'])
        usd_value = float(usd_bid['bid'])

        usd = float(name_assets * usd_value)
        # print(usd)
        usd_list.append(usd)
        bid_list.append(bid)
        '''
        # alternate method
        bid = base.loc[base['baseCurrency'] == i]
        bid = bid.filter(['bid'])
        bid_value = float(bid['bid'])
        print(bid_value) 
        '''
    print("-------------------------------")
    large = max(usd_list)
    final_bid = bid_list[usd_list.index(large)]
    index = usd_list.index(large)
    base_cur = name_list[index]
    # print(base_cur)
    name = base_cur + '/' + crypto
    print(name)
    # print(large)

    value_assets = (usdtbal-1) / final_bid

    placeoder(name, final_bid, value_assets, 'buy')
    name = base_cur + '/USD'

    final_bid_1 = usd_bid = usd_d.loc[usd_d['baseCurrency'] == base_cur]
    final_bid_1 = final_bid_1.filter(['bid'])
    final_bid = float(final_bid_1['bid'])

    value_assets = wall(base_cur)

    placeoder(name, final_bid, value_assets, 'sell')

    name = 'USDT/USD'
    bal1 = wall('USD')  # ftx_client.get_total_account_usd_balance()
    print(bal1)

    usd_value1 = usd_d.loc[usd_d['baseCurrency'] == 'USDT']
    usd_value1 = usd_value1.filter(['bid'])
    usd_value = float(usd_value1['bid'])

    #print(usd_value)
    value_assets = bal1 / usd_value
    placeoder(name, usd_value, value_assets, 'buy')
