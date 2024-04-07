from flask import Flask, render_template, jsonify
from dashapp import create_dash_application  # Assume que você tenha esta função

app = Flask(__name__)

dash = create_dash_application(app)

# Supondo que você tenha essas funções definidas no seu backend
def get_buy_price():
    # Retorna um valor fictício de compra. Substitua pela sua lógica de backend.
    return {"buyPrice": 67692.603}

def get_sell_price():
    # Retorna um valor fictício de venda. Substitua pela sua lógica de backend.
    return {"sellPrice": 67650.038}

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

