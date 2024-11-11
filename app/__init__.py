from flask import Flask
from config import Config
from routes import main as main_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(main_blueprint)

    return app
