from flask import Flask, render_template, jsonify
from dashapp import create_dash_application  # Assume que você tenha esta função

from trading_bot import Trading_bot
from wallet import Wallet


app = Flask(__name__)
bot = Trading_bot(Wallet(1000), cycles=5, secs=10)
#dash = create_dash_application(app)

@app.route('/price_change')
def price_change():
    # Substitua essa lógica pela sua lógica de backend para calcular a mudança de preço
    # Retorna um valor fictício de mudança de preço e porcentagem de mudança.
    # Por exemplo: +165,4 (+0.03%)
    return jsonify({"priceChange": "+165,4", "percentChange": "+0.03%", "direction": "🔼"})

# Supondo que você tenha essas funções definidas no seu backend
def get_buy_price():
    ask = bot.btc_bisk[1]
    return {"buyPrice": ask}

def get_sell_price():
    bid = bot.btc_bisk[0]
    return {"sellPrice": bid}

@app.route('/buy_price')
def buy_price():
    return jsonify(get_buy_price())

@app.route('/sell_price')
def sell_price():
    return jsonify(get_sell_price())

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

