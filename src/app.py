from flask import Flask, render_template, jsonify
from dashapp import create_dash_application  # Assume que você tenha esta função

from trading_bot import Trading_bot
from wallet import Wallet

app = Flask(__name__)
bot = Trading_bot(Wallet(1000), cycles=1, secs=2)
bot.start()
#dash = create_dash_application(app)

def get_buy_price():
    ask = bot.btc_bisk[1]
    return {"buyPrice": ask}

def get_wallet_USD():
    return {"wallet_USD": bot.wallet.get_usd()}

def get_wallet_BTC():
    return {"wallet_BTC": bot.wallet.get_btc()}

def get_sell_price():
    bid = bot.btc_bisk[0]
    return {"sellPrice": bid}

def get_price_change():
    result = ""
    return {"priceChange": result}

@app.route('/buy_price')
def buy_price():
    return jsonify(get_buy_price())

@app.route('/sell_price')
def sell_price():
    return jsonify(get_sell_price())

@app.route('/price_change')
def price_change():
    return jsonify(get_price_change())

@app.route('/wallet_USD')
def wallet_USD():
    return jsonify(get_wallet_USD())

@app.route('/wallet_BTC')
def wallet_BTC():
    return jsonify(get_wallet_BTC())

@app.route('/')
def index():
    return render_template('index.html')

bot_active = False

if __name__ == '__main__':
    if not bot_active:
        Trading_bot(Wallet(1000), cycles=1, secs=10)
        bot.start()
        app.run(debug=True)