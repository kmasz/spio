import dash
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader.data import DataReader
import time
from collections import deque
import plotly.graph_objs as go
import random

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1('Dash Bitcoin Test'),
    dcc.Graph(id='example',
              figure={
                  'data': [
                      {'x':[1,2,3,4,5], 'y':[4,6,3,7,6], 'type':'line', 'name':'boats'},
                      {'x':[1,2,3,4,5], 'y':[3,7,3,1,4], 'type':'bar', 'name':'cars'},
                  ],
              'layout': {
                  'title':'Basic Dash Example'
              }
              })
    ])

if __name__ == '__main__':
    app.run_server(debug=True)