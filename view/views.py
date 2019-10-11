#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template, redirect, url_for, request, session
from view._app import app
import json


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/addData', methods=['GET'])
def addData():
    if('username' not in session):
        return redirect(url_for('loginerr'))
    return render_template('addData.html')


@app.route('/loginerr')
def loginerr():
    return render_template('loginerr.html')


@app.route('/login')
def login():
    session['username'] = 'uname'
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/add', methods=['POST'])
def add():
    shop = request.form['shopName']
    machine = request.form['mNumber']
    adjust = request.form['adjustment']
    sudden = request.form['suddenValue']
    hidden = request.form['hiddenValue']
    green = request.form['greenValue']
    health = request.form['health']

    print(health)
    with open('json/data.json', 'r') as f:
        j = json.load(f)

    if shop not in j:
        j[shop] = {}

    j[shop][machine] = {}
    j[shop][machine]['adjust'] = adjust
    j[shop][machine]['sudden'] = sudden
    j[shop][machine]['hidden'] = hidden
    j[shop][machine]['green'] = green

    with open('json/data.json', 'w') as f:
        json.dump(j, f)

    return redirect(url_for('index'))
