# dashapp.py
import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd

# Suponha que 'df' é o seu DataFrame com os dados das velas
df = pd.DataFrame({
    'Date': pd.date_range(start='2021-01-01', periods=5, freq='D'),
    'Open': [100, 102, 104, 106, 108],
    'High': [105, 107, 109, 111, 113],
    'Low': [95, 97, 99, 101, 103],
    'Close': [102, 104, 106, 108, 110]
})

def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Candlestick", url_base_pathname='/dash/')
    
    # Crie o layout do gráfico de velas com os dados de 'df'
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                    open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close'])])
    
    # Define o layout do gráfico
    fig.update_layout(xaxis_rangeslider_visible=False)

    # Define o layout da aplicação Dash
    dash_app.layout = html.Div(children=[
        html.H1(children="Gráfico de Velas"),
        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])

    return dash_app
