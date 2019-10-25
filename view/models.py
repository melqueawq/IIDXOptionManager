#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ._app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class Option(db.Model):
    __tablename__ = 'option'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    shop_id = db.Column(db.Integer, db.ForeignKey(
        'shop.id', ondelete='CASCADE'))
    sudden = db.Column(db.Integer)
    hidden = db.Column(db.Integer)
    green = db.Column(db.Integer)
    adjustment = db.Column(db.Float)

    datetime = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        self.sudden = 0
        self.hidden = 0
        self.green = 0
        self.adjustment = 0.0

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Shop(db.Model):
    __tablename__ = 'shop'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    options = db.relationship('Shop', backref='option')
