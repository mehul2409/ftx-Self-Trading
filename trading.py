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
endpoint_url = 'https://ftx.com/api/markets'

# Get all market data as JSON
all_markets = requests.get(endpoint_url).json()
# Convert JSON to Pandas DataFrame
df = pd.DataFrame(all_markets['result'])
df.set_index('name', inplace=True)
df = df.filter(['name', 'baseCurrency', 'quoteCurrency', 'type', 'bid', 'change1h'])
dc = df.loc[df['type'] == 'spot']

c = dc["baseCurrency"].tolist()
print(c)