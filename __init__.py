#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Output, Event, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import sqlite3
import pandas as pd
import datetime
import time


app = dash.Dash(__name__) #TODO jak zmienić nazwę aplikacji i po co to w ogóle

conn1 = sqlite3.connect('cryptocurrency.db') #TODO zparametryzować nazwę bazy danych
df1 = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' ORDER BY 1 ASC", conn1)
df2 = pd.read_sql("SELECT * FROM bitcoin ORDER BY last_updated DESC", conn1)
available_crypto = df1['name'].unique()

app.layout = html.Div([  #TODO dodać cały layout strony
     html.H2('Live Cryptocurrency price'),
     html.Div([
         dcc.Dropdown(
             id='yaxis-column',
             options=[{'label': i, 'value': i} for i in available_crypto],
             value='bitcoin'
         )
     ]),
     dcc.Graph(id='live-graph', animate=True), #TODO przetestować czy nie wyłączyć animacji
     dcc.Interval(
         id='graph-update',
         interval=1*1000 #co jaki czas odświarza się strona
     ),
    dcc.Slider(
        id='date--slider',
        min=df2['last_updated'].min(),
        max=df2['last_updated'].max(),
        value=df2['last_updated'].max(),
        #min=0,
        #max=10,
        #value=10,
        step=None,
        marks={int(date): datetime.datetime.fromtimestamp(date).strftime('%m-%d %H:%M') for date in df2['last_updated'][::250].unique()}
        #marks={x: str(x)*3 for x in range(11)}
    ),
    html.H3(df2['last_updated'].count()),
    #html.H3(datetime.datetime.fromtimestamp(df2['last_updated'].min())),
    #html.H3(str(datetime.datetime.fromtimestamp(df2['last_updated'][0]))),
     ]
)

@app.callback(Output('live-graph', 'figure'),
              [Input(component_id='yaxis-column', component_property='value'),
               Input(component_id='date--slider', component_property='value')],
              events=[Event('graph-update', 'interval')])
def update_graph_scatter(available_crypto, date_value):
    try:
        ####  DEV  ####
        conn = sqlite3.connect('cryptocurrency.db') #TODO zparametryzować nazwę bazy danych
        ####  PROD  ####
        #conn = sqlite3.connect('/var/www/FlaskApp/FlaskApp/cryptocurrency.db') #TODO zparametryzować nazwę bazy danych
        #query = "SELECT * FROM " + available_crypto + " ORDER BY last_updated DESC LIMIT 200"
        query = "SELECT * FROM " + available_crypto + " ORDER BY last_updated DESC"
        df = pd.read_sql(query, conn)
        df.sort_values('last_updated', inplace=True) # sortowanie danych wg. czasu
        df['date'] = pd.to_datetime(df['last_updated'], unit='s', utc=True) #zamiana unix_na datę-czas
        dff = df[df['last_updated'] < date_value]
        with open('test.txt', 'a') as f:
            f.write(str(datetime.datetime.fromtimestamp(time.time())) + ': ' + str(date_value))
            f.write('\n')
        dff.set_index('date', inplace=True) #dodanie lidexu na datę-czas
#        df.index = df.index.tz_convert('Europe/Warsaw')
        #X = df.index[-200:] #pobpranie tylko 100 najświerzsych wpisów
        X = dff.index[-date_value:]
        #Y = df.price_usd.values[-200:]
        Y = dff.price_usd.values[-date_value:]

        data = plotly.graph_objs.Scatter(
            x=X,
            y=Y,
            name='Scatter',
            mode='lines+markers'
            #fill = "tozeroy",
            #fillcolor = "#6897bb"
        )

        return {'data': [data],'layout': go.Layout(
            xaxis=dict(range=[min(X),max(X)], title=available_crypto),
            yaxis=dict(range=[min(Y),max(Y)], title='price'),
            margin={'l': 70, 'b': 35, 't': 30, 'r': 50},
        )}

    except Exception as e:
        ####  DEV  ####
        with open('errors.txt', 'a') as f:
        ####  PROD  ####
        #with open('/var/www/FlaskApp/FlaskApp/errors.txt', 'a') as f:
            f.write(str(datetime.datetime.fromtimestamp(time.time())) + ': '+ str(e))
            f.write('\n')

####  PROD ####
#server = app.server


if __name__ == '__main__':
    app.run_server(debug=True)
