# app.py
from flask import Flask, render_template
from dashapp import create_dash_application  # Certifique-se de ter a função que cria a aplicação Dash

app = Flask(__name__)

# Crie a aplicação Dash e registre-a com o servidor Flask
dash_app = create_dash_application(app)

@app.route('/')
def index():
    # Renderiza o template 'index.html'
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

