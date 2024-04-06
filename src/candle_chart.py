from candle import Candle

# Classe de gráfico de vela
class Candle_chart:

    # Inicialização parametrizada
    def __init__(self, candles : list[Candle], cycles : int) -> None:
        self.candles = candles          # candles: lista de velas, candles[0] é a vela mais recente
        self.cycles = cycles            # cycles: número de ciclos por vela
        self.ema = self.alg_sma(12)     # ema: valor da média móvel exponencial

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
    def avg_pos(self, ipos : int, epos : int) -> float:
        return sum([candle.get_avg() for candle in self.candles[ipos:epos]]) / (epos - ipos)

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
            if delta > 0:
                gain += delta
            else:
                loss -= delta
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

# Teste
candle_l = [Candle(1, 2, 0.5, 1.5), Candle(1.5, 2.5, 1, 2), Candle(2, 3, 1.5, 2.5),
            Candle(2.5, 3.5, 2, 3), Candle(3, 8.5, 2.5, 7.5), Candle(7.5, 4.5, 3, 4),
            Candle(4, 5, 3, 3.5), Candle(3.5, 4.5, 3, 4), Candle(4, 5, 3.5, 4.5),
            Candle(4.5, 5.5, 4, 5), Candle(5, 6, 4.5, 5.5), Candle(5.5, 6.5, 5, 6),
            Candle(6, 7, 4, 4), Candle(4, 5, 3, 3.5), Candle(3.5, 4.5, 3, 3)]
c = Candle_chart(candles = candle_l, cycles = 5)

print(c.alg_ema(5, 1))
print(c.alg_rsi(1))