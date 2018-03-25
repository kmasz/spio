import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Event
from pandas_datareader.data import DataReader
from collections import deque
import plotly.graph_objs as go
import plotly
import json
from urllib import request
import pandas as pd
from datetime import datetime

#app = dash.Dash()

dataLink = 'https://api.coinmarketcap.com/v1/ticker/'

data = request.urlopen(dataLink)
data = data.read().decode("utf-8")
data = json.loads(data)
data = pd.DataFrame(data)
ids = data[data['id'] == 'bitcoin']
sss = datetime.utcfromtimestamp(int(ids['last_updated'][0]))

X = deque(maxlen=20)
X.append(datetime.now())
Y = deque(maxlen=20)
Y.append('11360.9')


app = dash.Dash(__name__)
app.layout = html.Div(
    [html.H3(str(sss) +'---'+ str(ids['price_usd'][0])),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*40000
        )
    ]
)
@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    X.append(sss)####
    Y.append(ids['price_usd'][0])####
    data = plotly.graph_objs.Scatter(
        x = list(X),
        y = list(Y),
        name = 'Scatter',
        mode = 'lines+markers'
    )

    return {'data':[data], 'layout': go.Layout(xaxis=dict(range=[min(X),max(X)]),
    yaxis=dict(range=[min(Y),max(Y)]),)}


'''app.layout = html.Div(children=[
    html.H1('Dash Bitcoin Test'),
    html.H3(str(sss) +'---'+ str(ids['price_usd'][0])),
    dcc.Graph(id='example',
              figure={
                  'data': [
                      #{'x':[1,2,3,4,5], 'y':[4,6,3,7,6], 'type':'line', 'name':'boats'},
                     # {'x':[1,2,3,4,5], 'y':[3,7,3,1,4], 'type':'bar', 'name':'cars'},
                      {'x': [sss], 'y':[ids['price_usd'][0]], 'type':'scatter', 'name':'bitcoin'}
                  ],
              'layout': {
                  'title':'Basic Dash Example'
              }
              })
    ])
'''
if __name__ == '__main__':
    app.run_server(debug=True)