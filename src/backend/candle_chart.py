from backend.candle import Candle

# Classe de gráfico de vela
class Candle_chart:

    # Inicialização parametrizada
    def __init__(self, candles : list[tuple[float, float, float, float]], cycles : int, obv : int) -> None:
        self.candles = [Candle(o, h, l, c)          # candles: lista de velas, candles[0] é a vela mais recente
                        for o, h, l, c in candles]
        self.cycles = cycles                        # cycles: número de ciclos por vela
        self.ema = self.alg_sma(12)                 # ema: valor da média móvel exponencial
        self.obv = obv                              # obv: valor do on balance volume

    # Gets
    def get_candles(self) -> list:
        return [(candle.get_open(), candle.get_high(),
                 candle.get_low(), candle.get_close())
                for candle in self.candles]
        
    # Adição da vela mais recententemente capturada
    def add_candle(self, svalue : float) -> None:
        value = float(svalue)
        self.candles.insert(0, Candle(value, value, value, value))
        # TODO self.candles.pop()
        return
    
    def update_candle(self, value : float) -> None:
        self.candles[0].feed(float(value))
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
    def alg_rsi(self, candles : int, frame = 1) -> float:
        gain = 0
        loss = 0
        for i in range (0, candles):
            close_pr = self.candles[i * frame].get_close()
            open_pr = self.candles[i * frame].get_open()
            delta = close_pr - open_pr
            if delta > 0:   gain += delta
            else:           loss -= delta
        gain = gain / candles
        loss = loss / candles
        if loss == 0:
            return 50
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    # Cálculo do EMA
    def alg_ema(self, candles : int) -> float:
        k = 2 / (candles + 1)
        now_pr = self.candles[0].get_close()
        self.ema = now_pr * k + self.ema * (1 - k)
        return self.ema
    
    # Cálculo do MACD
    def alg_macd(self) -> float:
        mline = self.alg_ema(12) - self.alg_ema(26)
        sline = self.alg_ema(9) - self.alg_ema(12)
        return mline - sline

    # Cálculo do Fibonacci
    def alg_fib_d(self, candles : int) -> float:
        min_pr, max_pr = self.min_max(epos = candles)
        amp = max_pr - min_pr
        dif = self.candles[0].get_close() - min_pr
        res = dif / amp
        if res < 0.236: return 0.236
        if res < 0.382: return 0.382
        if res < 0.5: return 0.5
        if res < 0.618: return 0.618
        if res < 0.786: return 0.786
        return 1

    # Cálculo do Fibonacci, contínuo
    def alg_fib_c(self, candles : int) -> float:
        min_pr, max_pr = self.min_max(epos = candles)
        amp = max_pr - min_pr
        dif = self.candles[0].get_close() - min_pr
        return dif / amp
    
    # Cálculo do OBV
    def alg_obv(self, volume : int, frames = 1) -> int:
        cond = self.candles[0].get_close() > self.candles[frames].get_close() 
        if self.candles[0].get_close() == self.candles[frames].get_close():
            return self.obv

        if cond:    self.obv = self.obv + volume
        else:       self.obv = self.obv - volume
        return self.obv
