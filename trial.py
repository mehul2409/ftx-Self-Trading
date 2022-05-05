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
bal = ftx_client.get_all_balances()
#print(bal)



global usdtbal
usdtbal1=bal['main']
for i in range(len(usdtbal1)):
    usdtbal2=usdtbal1[i]
    if(usdtbal2['coin']=='USDT'):
        usdtbal=usdtbal2['total']
        break
print(usdtbal)

