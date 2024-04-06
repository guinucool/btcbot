from candle import Candle

# Classe de gráfico de vela
class Candle_chart:

    # Inicialização parametrizada
    def __init__(self, candles : list[Candle], cycles : int) -> None:
        self.candles = candles          # candles: lista de velas, candles[0] é a vela mais recente
        self.cycles = cycles            # cycles: número de ciclos por vela

    # Adição da vela mais recententemente capturada
    def add_candle(self, candle : Candle) -> None:
        self.candles.insert(0, candle)
        # TODO self.candles.pop()
        return
    
    