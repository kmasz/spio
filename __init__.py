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


app = dash.Dash(__name__) #TODO jak zmienić nazwę aplikacji i po co to w ogóle
app.layout = html.Div(  #TODO dodać cały layout strony
    [html.H2('Live Bitcoin price'),
     dcc.Graph(id='live-graph', animate=True), #TODO przetestować czy nie wyłączyć animacji
     dcc.Interval(
         id='graph-update',
         interval=1*1000 #co jaki czas odświarza się strona
     ),
     ]
)

@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    try:
        ####  DEV  ####
        conn = sqlite3.connect('cryptocurrency.db') #TODO zparametryzować nazwę bazy danych
        ####  PROD  ####
        #conn = sqlite3.connect('/var/www/FlaskApp/FlaskApp/cryptocurrency.db') #TODO zparametryzować nazwę bazy danych
        df = pd.read_sql("SELECT * FROM bitcoin ORDER BY last_updated DESC LIMIT 200", conn) #TODO dodać możliwośc wyboru różnyhc kryptowalut
        df.sort_values('last_updated', inplace=True) # sortowanie danych wg. czasu
        df['date'] = pd.to_datetime(df['last_updated'], unit='s', utc=True) #zamiana unix_na datę-czas
        df.set_index('date', inplace=True) #dodanie lidexu na datę-czas
#        df.index = df.index.tz_convert('Europe/Warsaw')
        X = df.index[-100:] #pobpranie tylko 100 najświerzsych wpisów
        Y = df.price_usd.values[-100:]

        data = plotly.graph_objs.Scatter(
            x=X,
            y=Y,
            name='Scatter',
            mode='lines+markers'
        )

        return {'data': [data],'layout': go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                               yaxis=dict(range=[min(Y),max(Y)]),)}

    except Exception as e:
        ####  DEV  ####
        with open('errors.txt', 'a') as f:
        ####  PROD  ####
        #with open('/var/www/FlaskApp/FlaskApp/errors.txt', 'a') as f:
            f.write(str(e))
            f.write('\n')

####  PROD ####
#server = app.server


if __name__ == '__main__':
    app.run_server(debug=True)
