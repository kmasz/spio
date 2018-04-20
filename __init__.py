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
import configparser


###CONFIG PART
config = configparser.ConfigParser()
if config.read('config/config.conf'):
    ## DEV
    server_type = config['DEFAULT']['servertype']
elif config.read('/var/www/FlaskApp/FlaskApp/config/config.conf'):
    ## PROD
    server_type = config['DEFAULT']['servertype']
else:
    pass ##TODO dorobić obsługę błędu

db_file = config[server_type]['db_source'] #path to db file



app = dash.Dash(__name__) #TODO jak zmienić nazwę aplikacji i po co to w ogóle

####  DEV  ####
conn1 = sqlite3.connect(db_file)
####  PROD  ####
#conn1 = sqlite3.connect(db_file)
df1 = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' ORDER BY 1 ASC", conn1)
df2 = pd.read_sql("SELECT * FROM bitcoin ORDER BY last_updated DESC", conn1)
conn1.close()
available_crypto = df1['name'].unique()
date_marks = {}
df2['date'] = pd.to_datetime(df2['last_updated'], unit='s', utc=True)
for i in range(df2['date'].count()): #TODO czy da się zrobić dynamicznie wczytywany słwnik z markerami (niektóre kryptowaluty maja krótszą żywotność)
    if i == 0:
        date_marks[int(df2['last_updated'][i])] = df2['date'][i].strftime('%m-%d')
    else:
        if df2['date'][i-1].strftime('%m-%d') != df2['date'][i].strftime('%m-%d'):
            date_marks[int(df2['last_updated'][i])] = df2['date'][i].strftime('%m-%d')



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
    dcc.RangeSlider(
        id='date--slider',
        min=df2['last_updated'].min(),
        max=df2['last_updated'].max(),
        value=[df2['last_updated'].min(), df2['last_updated'].max()],
        #min=0,
        #max=10,
        #value=10,
        #step=6000,
        #dots=True,
        #pushable=50,
        allowCross=False,
        marks=date_marks
        #marks={int(date): datetime.datetime.fromtimestamp(date).strftime('%m-%d %H:%M') for date in df2['last_updated'][::250].unique()} #TODO zbudować ładny słownik markerów z dniami
        #marks={x: str(x)*3 for x in range(11)}
    ),
    #html.H3(date_marks['03-22']),
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
        conn = sqlite3.connect(db_file) #TODO zparametryzować nazwę bazy danych
        ####  PROD  ####
        #conn = sqlite3.connect(db_file) #TODO zparametryzować nazwę bazy danych
        #query = "SELECT * FROM " + available_crypto + " ORDER BY last_updated DESC LIMIT 200"
        query = "SELECT * FROM " + available_crypto + " ORDER BY last_updated DESC"
        df = pd.read_sql(query, conn)
        df.sort_values('last_updated', inplace=True) # sortowanie danych wg. czasu
        df['date'] = pd.to_datetime(df['last_updated'], unit='s', utc=True) #zamiana unix_na datę-czas
        dff = df[df['last_updated'] < date_value[1]]
        dfff = dff[dff['last_updated'] > date_value[0]]
        #with open('test.txt', 'a') as f:
        #    f.write(str(datetime.datetime.fromtimestamp(time.time())) + ': ' + str(date_value))
        #    f.write('\n')
        dfff.set_index('date', inplace=True) #dodanie lidexu na datę-czas
#        df.index = df.index.tz_convert('Europe/Warsaw')
        #X = df.index[-200:] #pobpranie tylko 100 najświerzsych wpisów
        X = dfff.index[-date_value[1]:]
        #Y = df.price_usd.values[-200:]
        Y = dfff.price_usd.values[-date_value[1]:]

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
