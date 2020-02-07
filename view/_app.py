#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
from flask_scss import Scss

from .config import SECRET_KEY

app = Flask(__name__, template_folder='../templates',
            static_folder="../static")
app.debug = True
Scss(app, static_dir='static', asset_dir='assets')

app.secret_key = SECRET_KEY
