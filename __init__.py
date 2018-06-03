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

####  DEV  ####
conn1 = sqlite3.connect('cryptocurrency.db')


currencies_select = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' ORDER BY 1 ASC", conn1)
bitcoin_quotes = pd.read_sql("SELECT * FROM bitcoin ORDER BY last_updated DESC", conn1)
conn1.close()
available_crypto = currencies_select['name'].unique()

offsets = {'quarter': 900, 'hour': 3600, '4hours': 14400, 'day': 86400, 'week': 604800}
offset = 'day'
date_marks = {}
bitcoin_quotes['date'] = pd.to_datetime(bitcoin_quotes['last_updated'], unit='s', utc=True)
for quote in range(bitcoin_quotes['date'].count()): #TODO czy da się zrobić dynamicznie wczytywany słwnik z markerami (niektóre kryptowaluty maja krótszą żywotność)
    if quote == 0:
        date_marks[int(bitcoin_quotes['last_updated'][quote])] = bitcoin_quotes['date'][quote].strftime('%m-%d')
    else:
        if bitcoin_quotes['date'][quote-1].strftime('%m-%d') != bitcoin_quotes['date'][quote].strftime('%m-%d'):
            date_marks[int(bitcoin_quotes['last_updated'][quote])] = bitcoin_quotes['date'][quote].strftime('%m-%d')


app.layout = html.Div([  #TODO dodać cały layout strony
     html.H2('Live Cryptocurrency price',
             style={'textAlign': 'center',
                    "color": "#354b5e"}),
     html.Div([
         dcc.Dropdown(
             id='yaxis-column',
             options=[{'label': crypto, 'value': crypto} for crypto in available_crypto],
             value='bitcoin'
         )
     ],
        style={"width": "35%",
               "display": "inline-block",
               "margin": "2% 7% 2% 8%"}),
     html.Div([
         dcc.Dropdown(
             id='time-offset',
             options=[
                {'label': '15 minutes', 'value': 'quarter'},
                {'label': '1 hour', 'value': 'hour'},
                {'label': '4 hours', 'value': '4hours'},
                {'label': '1 day', 'value': 'day'},
                {'label': '1 week', 'value': 'week'}
             ],
             value='quarter',
         )
     ],
        style={"width": "35%",
               "display": "inline-block",
               "margin": "2% 8% 2% 7%"}),
     dcc.Graph(id='live-graph', animate=True), #TODO przetestować czy nie wyłączyć animacji
     dcc.Interval(
         id='graph-update',
         interval=1*1000 #co jaki czas odświeża się strona
     )],
     style={"backgroundColor": "#fffefe",
            "fontFamily": "Calibri",
            "color": "#354b5e",
            "width": "84%",
            "marginLeft": "auto",
            "marginRight": "auto"}
)


@app.callback(Output('live-graph', 'figure'),
              [Input(component_id='yaxis-column', component_property='value'),
               Input(component_id='time-offset', component_property='value')],
              events=[Event('graph-update', 'interval')])
def update_graph_scatter(selected_crypto, date_scope):
    offset = offsets[date_scope]
    try:
        ####  DEV  ####
        conn = sqlite3.connect('cryptocurrency.db') #TODO zparametryzować nazwę bazy danych
        query = "SELECT * FROM " + selected_crypto + " ORDER BY last_updated DESC"
        all_currencies_data = pd.read_sql(query, conn)
        all_currencies_data.sort_values('last_updated', inplace=True) # sortowanie danych wg. czasu
        updates_times = all_currencies_data['last_updated']
        oldest_record = updates_times.max() - offset if updates_times.max() - offset > updates_times.min() else updates_times.min()

        scoped_currencies = all_currencies_data.loc[all_currencies_data['last_updated'] > oldest_record]
        scoped_currencies['date'] = pd.to_datetime(updates_times, unit='s', utc=True) #zamiana unix_na datę-czas

        scoped_currencies.set_index('date', inplace=True) #dodanie lidexu na datę-czas
        X = scoped_currencies.index
        Y = scoped_currencies.price_usd.values

        data = plotly.graph_objs.Scatter(
            x=X,
            y=Y,
            name='Scatter',
            mode='lines+markers'
        )

        return {'data': [data],'layout': go.Layout(
            xaxis=dict(range=[min(X),max(X)], title=selected_crypto),
            yaxis=dict(range=[min(Y),max(Y)], title='price'),
            margin={'l': 70, 'b': 35, 't': 30, 'r': 50},
        )}

    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(datetime.datetime.fromtimestamp(time.time())) + ': ' + str(e))
            f.write('\n')

if __name__ == '__main__':
    app.run_server(debug=True)
