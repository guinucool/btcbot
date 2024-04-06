import threading
import time

import backend.api_caller as api
from backend.wallet import Wallet
from backend.candle_chart import Candle_chart

# Classe do trading bot
class Trading_bot:

    # Inicialização
    def __init__(self, wallet : Wallet, cycles = 5, secs = 10) -> None:
        print("bot: loading...")
        self.wallet = wallet                                            # wallet: carteira do bot
        self.rtable = api.Rate_table("BTC-USD")                         # rtable: tabela de preços, formato yf.Ticker.history
        self.rtable.get_rate_table("1mo", "2m")
        obv = self.rtable.get_last_obv()
        self.chart = Candle_chart(self.rtable.get_candles(), 2, obv)    # chart: gráfico de velas
        self.cycles = cycles                                            # cycles: número de ciclos por vela
        self.secs = secs                                                # secs: segundos por ciclo
        self.inds = {}                                                  # inds: indicadores
        # Customizables aqui
        return

    # Gets
    def get_ind(self) -> dict[float]:
        return self.inds
    
    def get_balance(self) -> tuple[float, float]:
        return self.wallet.get_usd(), self.wallet.get_btc()
    
    def get_chart(self) -> list:
        return self.chart.get_candles()
    
    def get_interval(self) -> int: # secs
        return self.secs * self.cycles

    # Transação
    def buy_btc(self, btc : float) -> bool:
        rate = api.get_rate_btc_usd_now("bid")
        try:
            self.wallet.add_transaction(btc, btc * rate, rate)
            return True
        except Exception as e:
            print("Error:", e)
        return False

    def sell_btc(self, btc : float) -> bool:
        rate = api.get_rate_btc_usd_now("ask")
        try:
            self.wallet.add_transaction(-btc, -btc * rate, rate)
            return True
        except Exception as e:
            print("Error:", e)
        return False

    # Ciclo de feed
    def cycle(self) -> None:
        i = 1
        ###
        counter = 0
        while True:
            #bid = api.get_rate_btc_usd_now("bid")
            bid = self.chart.candles[-i].get_close()
            if counter == self.cycles:
                counter = 0
                self.chart.add_candle(bid)
            else:
                counter += 1
                self.chart.update_candle(bid)
            time.sleep(self.secs)

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
    
    def start(self):
        print("bot: online")
        threading.Thread(target = lambda: self.cycle()).start()
        print("bot: cycle started")

# Teste
t = Trading_bot(Wallet(1000), secs=0.3)
t.start()
t.buy_btc(0.1)