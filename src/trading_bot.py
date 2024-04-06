import api_caller as api
from wallet import Wallet
from candle_chart import Candle_chart
from math import inf

counter = 0

# Classe do trading bot
class Trading_bot:

    # Inicialização
    def __init__(self, wallet : Wallet, cycles = 5, secs = 10) -> None:
        self.wallet = wallet                                            # wallet: carteira do bot
        self.rtable = api.Rate_table("BTC-USD")                         # rtable: tabela de preços, formato yf.Ticker.history
        self.rtable.get_rate_table("1mo", "2m")
        obv = self.rtable.get_last_obv()
        self.chart = Candle_chart(self.rtable.get_candles(), 2, obv)    # chart: gráfico de velas
        self.cycles = cycles                                            # cycles: número de ciclos por vela
        self.secs = secs                                                # secs: segundos por ciclo
        self.inds = {}                                                  # inds: indicadores
        return

    # Ciclo de feed
    def cycle(self) -> None:
        global counter
        global i
        #bid = api.get_rate_btc_usd_now("bid")
        bid = self.chart.candles[-i].get_close()
        if counter == self.cycles:
            counter = 0
            self.chart.add_candle(bid)
        else:
            counter += 1
            self.chart.update_candle(bid)
        return

    # Cálculo de indicadores
    def cinds(self) -> dict[float]:
        inds = {
            "rsi" : self.chart.alg_rsi(14),
            "ema50" : self.chart.alg_ema(50),
            "ema100" : self.chart.alg_ema(100),
            "ema200" : self.chart.alg_ema(200),
            "fibc" : self.chart.alg_fib_c(100),
            "fibd" : self.chart.alg_fib_d(100),
            "obv" : self.chart.alg_obv(self.rtable.get_last_obv()),
            "macd" : self.chart.alg_macd(),
            "sma50" : self.chart.alg_sma(50),
            "sma100" : self.chart.alg_sma(100),
            "sma200" : self.chart.alg_sma(200)
        }
        self.inds = inds
        return inds

s = 0.1
i = 1
import time
print("bot: loading...")
bot = Trading_bot(Wallet(1000), secs=s)
print("bot: online")
while(True):
    bot.cycle()
    #print(bot.chart.candles[0].__str__())
    i += 1
    time.sleep(s)