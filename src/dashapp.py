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

def history_table(bot):
    hist = bot.wallet.get_history()
    return html.Table([
        html.Thead(
            html.Tr([html.Th("Data"), html.Th("USD"), html.Th("BTC"), html.Th("Taxa"), html.Th("Saldo USD"), html.Th("Saldo BTC")],
                    style={"color": "white"})
        ),
        html.Tbody([
            html.Tr([
                html.Td(hist[i]["date"]),
                html.Td(hist[i]["usd"]),
                html.Td(hist[i]["btc"]),
                html.Td(hist[i]["rate"]),
                html.Td(hist[i]["usd_balance"]),
                html.Td(hist[i]["btc_balance"]),
            ]) for i in range(len(hist))
        ], style={"color": "white"})
    ])

def create_dash_app(flask_app, bot):
    dash_app = dash.Dash(server=flask_app, name="Candlestick", url_base_pathname='/dash/')
    
    fig = go_figure(bot)
    fig.update_layout(xaxis_rangeslider_visible=False)
    table = history_table(bot)

    dash_app.layout = html.Div(children=[
        html.Div(children=[
            html.H1(children="Gráfico de Velas", style={"textAlign": "center", "color": "white"}),
            dcc.Graph(
            id='example-graph',
            figure=fig)]),
        html.Div(children=[
            html.H1(children="Histórico", style={"textAlign": "center", "color": "white"}),
            table])
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