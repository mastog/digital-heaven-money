import os

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from backend.config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(
    app,
    origins=["http://127.0.0.1:4321"],  # 支持多个地址
    supports_credentials=True,
)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

