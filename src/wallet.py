import datetime

# Classe de carteira
class Wallet:

    # Inicialização
    def __init__(self, balance : float) -> None:
        self.btc = 0
        self.usd = balance
        self.history = []
        self.history.append({
            "date": datetime.datetime.now(),
            "usd": 30,
            "btc": 30 / 63000,
            "rate": 63000,
            "usd_balance": balance,
            "btc_balance": 0
            })
        self.history.append({
            "date": datetime.datetime.now(),
            "usd": 40,
            "btc": 40 / 65000,
            "rate": 65000,
            "usd_balance": balance + 20,
            "btc_balance": 0
            })
        self.lim_btc = None
        self.lim_usd = None

    # Gets
    def get_btc(self) -> float:
        return self.btc
    
    def get_usd(self) -> float:
        return self.usd
    
    def get_history(self) -> list:
        return self.history
    
    # Sets
    def set_lim_btc(self, lim : float) -> None:
        self.lim_btc = lim
        return
    
    def set_lim_usd(self, lim : float) -> None:
        self.lim_usd = lim
        return

    # Adição de uma transação à carteira
    def add_transaction(self, btc : float, usd : float, rate : float) -> bool:
        if self.usd - usd < 0 or self.btc - btc < 0:
            raise Exception("[WALLET] Insufficient funds.")
        self.usd += usd
        self.btc += btc
        self.history.insert(0, {
            "date": datetime.datetime.now(),
            "usd": usd,
            "btc": btc,
            "rate": rate,
            "usd_balance": self.usd,
            "btc_balance": self.btc
            })
        return True