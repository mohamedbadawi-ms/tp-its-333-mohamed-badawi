from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alchemy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Try to enable Flasgger (Swagger UI). If it's not installed, keep the app functional and log a warning.
try:
    from flasgger import Swagger
    swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "API de Gestion des Étudiants",
            "description": "API pour gérer les étudiants avec SQLAlchemy",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "token",
                "in": "cookie"
            }
        }
    })
except ModuleNotFoundError:
    swagger = None
    logging.warning("Flasgger is not installed – Swagger UI will be disabled. Install with `pip install flasgger` or `pip install -r requirements.txt` in this folder.")

from app import views, models