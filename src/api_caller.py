import requests
import yfinance as yf

# Tabela de currencies específicas
def get_rate_table(tickers, period, interval) -> yf.Ticker.history:
    return yf.download(tickers = tickers, period = period, interval = interval)

# Retorna o preço do Bitcoin em USD, bisk = "ask" ou "bid"
# NOTE bid = preço mais alto que o comprador paga, ask = preço mais baixo que o vendedor aceita
def get_rate_btc_usd_now(bisk) -> float:
    response = requests.get("https://api.uphold.com/v0/ticker/BTC-USD")
    return response.json()[bisk]

# Retorna o fear and greed index
def get_fng() -> float:
    response = requests.get("https://api.alternative.me/fng/")
    return response.json()["data"][0]["value"]

# Classe que gere tabelas de preços
class Rate_table:

    # Inicialização
    def __init__(self, currency : str) -> None:
        self.ticker = yf.Ticker(currency)
        self.last_table = None
        yf.set_tz_cache_location("src/__pycache__/yfinance_cache")

    def get_last_table(self) -> yf.Ticker.history:
        return self.last_table
        
    # Carrega e Retorna uma tabela de preços do Bitcoin em USD no período e intervalo especificados
    # Intervalos suportados: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
    def get_rate_table(self, period : str, interval : str) -> yf.Ticker.history:
        self.last_table = self.ticker.history(period = period, interval = interval)
        return self.last_table

    # Retorna a última tabela de preços em formato de dicionário
    def get_dict_table(self) -> dict:
        res = {}
        for k in ["Open", "High", "Low", "Close"]:
            res[k] = self.last_table[k]
        return res

    # Devolução de uma lista de candles
    def get_candles(self) -> list:
        return [(self.last_table["Open"].iloc[i],
                self.last_table["High"].iloc[i],
                self.last_table["Low"].iloc[i],
                self.last_table["Close"].iloc[i])
                for i in range(len(self.last_table["Open"]))]

    def get_last_obv(self) -> int:
        if not self.last_table.empty:
            for i in self.last_table["Volume"]:
                if i != 0: return i
        table = self.get_rate_table("1d", "1d")
        if table["Volume"].any():
            return table["Volume"][0]
        return 35683977532
