import threading
import time

import api_caller as api
from wallet import Wallet
from candle_chart import Candle_chart

# Classe do trading bot
class Trading_bot:

    # Inicialização
    def __init__(self, wallet : Wallet, cycles = 5, secs = 10) -> None:
        print("bot: loading...")
        self.wallet = wallet                                            # wallet: carteira do bot
        self.rtable = api.Rate_table("BTC-USD")                         # rtable: tabela de preços, formato yf.Ticker.history
        self.rtable.get_rate_table("3d", "2m")
        obv = self.rtable.get_last_obv()
        self.chart = Candle_chart(self.rtable.get_candles(), 2, obv)    # chart: gráfico de velas
        self.cycles = cycles                                            # cycles: número de ciclos por vela
        self.secs = secs                                                # secs: segundos por ciclo
        self.inds = {}                                                  # inds: indicadores
        self.btc_bisk = 0, 0                                            # btc_price: bid e ask do Bitcoin
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
    
    def get_bisk(self) -> tuple[float, float]:
        return self.btc_bisk

    # Transações
    def sell_btc(self, btc : float) -> bool:
        rate = self.btc_bisk[0]
        try:
            self.wallet.add_transaction(-btc, -btc * rate, rate)
            return True
        except Exception as e:
            print("Error:", e)
        return False
    
    def buy_btc(self, btc : float) -> bool:
        rate = self.btc_bisk[1]
        try:
            self.wallet.add_transaction(btc, btc * rate, rate)
            return True
        except Exception as e:
            print("Error:", e)
        return False

    # Ciclo de feed
    def cycle(self, counter = 0) -> None:
        try:
            bid, ask = api.get_rate_btc_usd_now()
            self.btc_bisk = bid, ask
        except Exception as e:
            print("Error:", e)
            return counter
        if counter == self.cycles:
            counter = 0
            self.chart.add_candle(bid)
        else:
            counter += 1
            self.chart.update_candle(bid)
        return counter

    # Ciclo de execução
    def cycle_exec(self) -> None:
        counter = 0
        while True:
            counter = self.cycle(counter)
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
        cycle_thread = threading.Thread(target = lambda : self.cycle_exec())
        cycle_thread.start()
        print("bot: online")
