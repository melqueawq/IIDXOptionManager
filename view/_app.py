#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .config import SECRET_KEY

app = Flask(__name__, template_folder='../templates',
            static_folder="../static")

app.secret_key = SECRET_KEY
db = SQLAlchemy(app)
Migrate(app, db)


@app.before_first_request
def create_tables():
    from view.models import Option, Shop
    db.create_all()
