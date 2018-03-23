import dash
from dash.dependencies import Output, Event, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import sqlite3
import pandas as pd

conn = sqlite3.connect('cryptocurrency.db') #TODO zparametryzować nazwę bazy danych
df = pd.read_sql("SELECT last_updated FROM bitcoin ORDER BY last_updated DESC LIMIT 1", conn) #TODO dodać możliwośc wyboru różnyhc kryptowalut
df.sort_values('last_updated', inplace=True) # sortowanie danych wg. czasu
print(df)
print('*'*20)
df['date'] = pd.to_datetime(df['last_updated'], unit='s', utc=True) #zamiana unix_na datę-czas
#df['date'] = df['last_updated'].tz_localize('UTC').tz_convert('Europe/Warsaw')
#df['date'] = df['date'].tz_convert('Europe/Warsaw')
df.set_index('date', inplace=True) #dodanie lidexu na datę-czas
df.index = df.index.tz_convert('Europe/Warsaw')


print(df)
print('*'*20)
#print(df['last_updated'].tz_localize('UTC').tz_convert('Europe/Warsaw'))