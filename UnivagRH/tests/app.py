from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def PaginaInicial():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)