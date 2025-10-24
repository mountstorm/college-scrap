"""
Flask Application Factory
"""
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'sqlite:///collegescrap.db')

    # Enable CORS
    CORS(app)

    # Register blueprints
    from app.api.routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app
