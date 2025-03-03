import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "users.db")
app.config['SECRET_KEY'] = 'your-secret-key-here'
db = SQLAlchemy(app)

from backend import routes, models

#with app.app_context():
    #db.create_all()
app.run(debug=True)
