from flask import Flask
from dotenv import load_dotenv
from tests.ext.configuration import configure_all
import os

def create_app():

    load_dotenv()
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.secret_key = os.getenv('SECRET_KEY', 'meurhunivag')
    configure_all(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)