# Classe de vela
class Candle:

    # Inicialização parametrizada, para histórico
    def __init__(self, open : float, high : float, low : float, close : float) -> None:
        self.open = open
        self.high = high
        self.low = low
        self.close = close

    # Inicialização com valor único, para live rates
    def __init__(self, value : float) -> None:
        self.open = value
        self.high = value
        self.low = value
        self.close = value

    # Atualização a vela com um novo valor
    def feed(self, value : float) -> None:
        self.close = value
        if value > self.high:
            self.high = value
        elif value < self.low:
            self.low = value

    # Gets
    def get_open(self) -> float:
        return self.open
    
    def get_close(self) -> float:
        return self.close
    
    def get_high(self) -> float:
        return self.high
    
    def get_low(self) -> float:
        return self.low

    # ToString
    def __str__(self) -> str:
        return f"Open: {self.open}, High: {self.high}, Low: {self.low}, Close: {self.close}"
