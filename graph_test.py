import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
import sqlite3
import pandas as pd

app = dash.Dash(__name__)
app.layout = html.Div(
    [html.H2('Live Bitcoin price'),
     dcc.Graph(id='live-graph', animate=True),
     dcc.Interval(
         id='graph-update',
         interval=1*1000
     ),
     ]
)

@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    try:
        conn = sqlite3.connect('cryptocurrency.db')
        c = conn.cursor()
        df = pd.read_sql("SELECT * FROM bitcoin ORDER BY last_updated DESC LIMIT 100", conn)
        df.sort_values('last_updated', inplace=True)
        df['date'] = pd.to_datetime(df['last_updated'], unit='s')
        df.set_index('date', inplace=True)

        X = df.index[-100:]
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
        with open('errors.txt', 'a') as f:
            f.write(str(e))
            f.write('\n')


if __name__ == '__main__':
    app.run_server(debug=True)