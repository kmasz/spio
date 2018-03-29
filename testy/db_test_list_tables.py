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

conn = sqlite3.connect('../cryptocurrency.db')
#df1 = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
#available_cryptocurrency = df1['Name']
#print (df1['name'])
available_crypto = u"0x"
query = "SELECT * FROM " + available_crypto + " ORDER BY last_updated DESC LIMIT 1"
df = pd.read_sql(query, conn)
#df = pd.read_sql("SELECT * FROM ? ORDER BY ? DESC LIMIT ?", conn, params=[available_crypto, 'last_updated', 4])
#df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE %s ORDER BY unix DESC LIMIT 1000", conn ,params=[sentiment_term,])
print(df)