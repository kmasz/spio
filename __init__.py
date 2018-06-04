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
    pass  ##TODO dorobić obsługę błędu

db_file = config[server_type]['db_source']  # path to db file

app = dash.Dash(__name__)  # TODO jak zmienić nazwę aplikacji i po co to w ogóle

####  DEV  ####
conn1 = sqlite3.connect(db_file)
####  PROD  ####
# conn1 = sqlite3.connect(db_file)
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
        if bitcoin_quotes['date'][quote - 1].strftime('%m-%d') != bitcoin_quotes['date'][quote].strftime('%m-%d'):
            date_marks[int(bitcoin_quotes['last_updated'][quote])] = bitcoin_quotes['date'][quote].strftime('%m-%d')

app.layout = html.Div([  #TODO dodać cały layout strony
<<<<<<< HEAD
     html.H2('Live Cryptocurrency price',
             style={'textAlign': 'center',
                    "color": "#354b5e"}),
=======
     html.H2('Live Bitcoin price'),
>>>>>>> 6dfc45b54dd3efc809ec3cb2b41bb32ce004df23
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
         interval=10*1000 #co jaki czas odświeża się strona
     ),
     html.Div([
         html.H3("[Knowledge base] Cryptocurrencies 101"),
         html.P('A cryptocurrency is a medium of exchange like normal currencies such as USD, but designed for the'
                ' purpose of exchanging digital information through a process made possible by certain principles of'
                ' cryptography. Cryptography is used to secure the transactions and to control the creation of new'
                ' coins. The first cryptocurrency to be created was Bitcoin back in 2009.',
               className='article',
               id='regulations'),
         html.A("Read more",
                href='https://www.ccn.com/cryptocurrency/',
                target='blank')
         ],
         style={"width": "25%",
                "margin": "2% 4%",
                "display": "inline-block"}),
     html.Div([
         html.H3("[Law] Legal landscape around cryptos"),
         html.P('As demand for cryptocurrency grows, global regulators are divided on how to keep up. '
               'Most digital currencies are not backed by any central government, meaning each country '
               'has different standards. Every seemingly small regulation announcement has driven the price of '
               'bitcoin and other cryptocurrencies in 2018. Here\'s your guide to where digital currencies stand '
               'with governments and regulators around the globe.',
               className='article',
               id='regulations'),
         html.A("Read more",
                href='https://www.cnbc.com/2018/03/27/a-complete-guide-to-cyprocurrency-regulations-around-the-world.html',
                target='blank')
         ],
         style={"width": "25%",
                "margin": "2% 4%",
                "display": "inline-block"}),
     html.Div([
         html.H3("[Opinions] What to invest in"),
         html.P('The financial world is changing, that’s something that many people have come to realize as solutions'
                ' like cryptocurrency and Bitcoin take over traditional cash and stocks. Now that we’re finally in 2018,'
                ' it’s safe to say that the crypto markets are stronger than ever, with more opportunities for'
                ' investment on the way. Stellar Lumens, IOTA, and EOS are all big winners in the current marketplace,'
                ' and there are plenty of additional options to consider too.',
               className='article',
               id='regulations'),
         html.A("Read more",
                href='https://www.mineweb.net/best-cryptocurrency-to-invest-in-2018',
                target='blank')
         ],
         style={"width": "25%",
                "margin": "2% 4%",
                "display": "inline-block"})],

     style={'backgroundColor': '#fffefe',
            "fontFamily": "Calibri",
            "color": "#354b5e",
            "width": "84%",
            "marginLeft": "auto",
            "marginRight": "auto"}
)


@app.callback(Output('live-graph', 'figure'),
<<<<<<< HEAD
              [Input(component_id='yaxis-column', component_property='value'),
               Input(component_id='time-offset', component_property='value')],
              events=[Event('graph-update', 'interval')])
def update_graph_scatter(selected_crypto, date_scope):
    offset = offsets[date_scope]
=======
              [Input(component_id='yaxis-column', component_property='value')],
              events=[Event('graph-update', 'interval')])
def update_graph_scatter(available_crypto):
>>>>>>> 6dfc45b54dd3efc809ec3cb2b41bb32ce004df23
    try:
        ####  DEV  ####
        conn = sqlite3.connect(db_file)  # TODO zparametryzować nazwę bazy danych
        ####  PROD  ####
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

<<<<<<< HEAD
        return {'data': [data], 'layout': go.Layout(
            xaxis=dict(range=[min(X), max(X)], title=selected_crypto),
            yaxis=dict(range=[min(Y), max(Y)], title='price'),
            margin={'l': 70, 'b': 35, 't': 30, 'r': 50},
        )}
=======
        return {'data': [data],'layout': go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                               yaxis=dict(range=[min(Y),max(Y)]),)}
>>>>>>> 6dfc45b54dd3efc809ec3cb2b41bb32ce004df23

    except Exception as e:
        ####  DEV  ####
        with open('errors.txt', 'a') as f:
            ####  PROD  ####
            f.write(str(datetime.datetime.fromtimestamp(time.time())) + ': ' + str(e))
            f.write('\n')

#external_css = ["https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"]
#for css in external_css:
#    app.css.append_css({"external_url": css})


####  PROD ####
if server_type == 'PROD':
    server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
