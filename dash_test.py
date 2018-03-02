import dash
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader.data import DataReader
import time
from collections import deque
import plotly.graph_objs as go
import random
import json
from urllib import request
import pandas as pd
import datetime

app = dash.Dash()

dataLink = 'https://api.coinmarketcap.com/v1/ticker/'

data = request.urlopen(dataLink)
data = data.read().decode("utf-8")
data = json.loads(data)
data = pd.DataFrame(data)
ids = data[data['id'] == 'bitcoin']

app.layout = html.Div(children=[
    html.H1('Dash Bitcoin Test'),
    html.H3(str(ids['last_updated'][0]) +'---'+ str(ids['price_usd'][0])),
    dcc.Graph(id='example',
              figure={
                  'data': [
                      #{'x':[1,2,3,4,5], 'y':[4,6,3,7,6], 'type':'line', 'name':'boats'},
                     # {'x':[1,2,3,4,5], 'y':[3,7,3,1,4], 'type':'bar', 'name':'cars'},
                      {'x':[ids['last_updated'][0]], 'y':[ids['price_usd'][0]], 'type':'line', 'name':'bitcoin'}
                  ],
              'layout': {
                  'title':'Basic Dash Example'
              }
              })
    ])

if __name__ == '__main__':
    app.run_server(debug=True)