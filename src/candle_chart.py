from candle import Candle

# Classe de gráfico de vela
class Candle_chart:

    # Inicialização parametrizada
    def __init__(self, candles : list[Candle], cycles : int, obv = 62277632) -> None:
        self.candles = candles          # candles: lista de velas, candles[0] é a vela mais recente
        self.cycles = cycles            # cycles: número de ciclos por vela
        self.ema = self.alg_sma(12)     # ema: valor da média móvel exponencial
        self.obv = obv                  # obv: valor do on balance volume

    # Adição da vela mais recententemente capturada
    def add_candle(self, candle : Candle) -> None:
        self.candles.insert(0, candle)
        # TODO self.candles.pop()
        return
    
    # NOTE Frame é o número de velas no intervalo
    # Cálculo de frame no intervalo especificado em segundos
    def time_pos(self, time : int) -> int:
        return time // self.cycles
    
    # Cálculo de frame através de ciclos
    def time_frames(self, cycles : int) -> int:
        if cycles < self.cycles:
            return 1
        return cycles // self.cycles

    # Média de velas entre posições
    def avg_pos(self, epos : int, ipos = 0) -> float:
        return sum([candle.get_avg() for candle in self.candles[ipos:epos]]) / (epos - ipos)

    # Minimo e máximo de um número de velas
    def min_max(self, epos : int, ipos = 0,) -> tuple[float, float]:
        return (min([candle.get_low() for candle in self.candles[ipos:epos]]),
                max([candle.get_high() for candle in self.candles[ipos:epos]]))

    # Cálculo do SMA para um número de velas
    def alg_sma(self, candles : int) -> float:
        return sum([candle.get_close() for candle in self.candles[:candles]]) / candles

    # Cálculo do RSI usando um frame
    def alg_rsi(self, frame : int) -> float:
        gain = 0
        loss = 0
        for i in range (0, 14):
            close_pr = self.candles[i * frame].get_close()
            open_pr = self.candles[i * frame].get_open()
            delta = close_pr - open_pr
            if delta > 0:   gain += delta
            else:           loss -= delta
        gain = gain / 14
        loss = loss / 14
        if loss == 0:
            return 50
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    # Cálculo do EMA
    def alg_ema(self, candles : int, frame : int) -> float:
        k = 2 / (candles + 1)
        now_pr = self.candles[0].get_close()
        self.ema = now_pr * k + self.ema * (1 - k)
        return self.ema
    
    # Cálculo do MACD
    def alg_macd(self, frame : int) -> float:
        mline = self.alg_ema(12, frame) - self.alg_ema(26, frame)
        sline = self.alg_ema(9, frame)
        return mline - sline

    # Cálculo do Fibonacci
    def alg_fib_d(self, frame : int) -> float:
        min_pr, max_pr = self.min_max(frame)
        ratio = min_pr / max_pr
        if ratio < 0.236: return 0.236
        elif ratio < 0.382: return 0.382
        elif ratio < 0.5: return 0.5
        elif ratio < 0.618: return 0.618
        elif ratio < 0.786: return 0.786
        return 1
    
    # Cálculo do Fibonacci, contínuo
    def alg_fib_c(self, frame : int) -> float:
        min_pr, max_pr = self.min_max(frame)
        ratio = min_pr / max_pr
        return ratio
    
    # Cálculo do OBV
    def alg_obv(self, volume : int, frames : int) -> int:
        cond = self.candles[0].get_close() > self.candles[frames].get_close() 
        if self.candles[0].get_close() == self.candles[frames].get_close():
            return self.obv

        if cond:    self.obv = self.obv + volume
        else:       self.obv = self.obv - volume
        return self.obv
