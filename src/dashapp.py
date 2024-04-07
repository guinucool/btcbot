# dashapp.py
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import dash

def go_figure(bot):
    candles = bot.get_chart()
    df = pd.DataFrame(candles)
    return go.Figure(data=[go.Candlestick(
                    open=df[0], high=df[1],
                    low=df[2], close=df[3])])

def create_dash_app(flask_app, bot):
    dash_app = dash.Dash(server=flask_app, name="Candlestick", url_base_pathname='/dash/')
    
    fig = go_figure(bot)
    fig.update_layout(xaxis_rangeslider_visible=False)

    dash_app.layout = html.Div(children=[
        html.H1(children="Gráfico de Velas"),
        dcc.Graph(
            id='example-graph',
            figure=fig)
        ])
    
    return dash_app

def update_dash_app(dash_app, bot):
    fig = go_figure(bot)
    fig.update_layout(xaxis_rangeslider_visible=False)

    dash_app.layout = html.Div(children=[
        html.H1(children="Gráfico de Velas"),
        dcc.Graph(
            id='example-graph',
            figure=fig)
        ])
    
    return dash_app