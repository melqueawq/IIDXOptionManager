#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
from .config import SECRET_KEY

app = Flask(__name__, template_folder='../templates',
            static_folder="../static")

app.secret_key = SECRET_KEY
