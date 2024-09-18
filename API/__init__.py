from flask import Flask
from .extensions import api, db, jwt
from .resources import ns
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token_cookie'  
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    
    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    
    api.add_namespace(ns)
    
    CORS(app, supports_credentials=True)

    return app
