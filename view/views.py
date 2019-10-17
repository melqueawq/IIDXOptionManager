#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template, redirect, url_for, request, session
from ._app import app
from .twmng import twitter_api
import json
import os


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/addData', methods=['GET'])
def addData():
    if('screen_name' not in session):
        return redirect(url_for('loginerr'))

    with open('json/' + session['screen_name'] + '.json', 'r') as f:
        j = json.load(f)

    return render_template('addData.html', json=j)


@app.route('/editData')
def editData():
    shopName = request.args.get('sn')
    machineName = request.args.get('mn')
    with open('json/' + session['screen_name'] + '.json', 'r') as f:
        j = json.load(f)

    option = j[shopName][machineName]

    return render_template('editData.html',
                           shopName=shopName,
                           machineName=machineName,
                           option=option)


@app.route('/delete')
def delete():
    shopName = request.args.get('sn')
    machineName = request.args.get('mn')
    with open('json/' + session['screen_name'] + '.json', 'r') as f:
        j = json.load(f)

    j[shopName].pop(machineName)
    if len(j[shopName]) == 0:
        j.pop[shopName]

    with open('json/' + session['screen_name'] + '.json', 'w') as f:
        json.dump(j, f)

    return redirect(url_for('stats'))


@app.route('/stats', methods=['GET'])
def stats():
    if('screen_name' not in session):
        return redirect(url_for('loginerr'))

    with open('json/' + session['screen_name'] + '.json', 'r') as f:
        j = json.load(f)

    return render_template('stats.html', json=j)


@app.route('/loginerr')
def loginerr():
    return render_template('loginerr.html')


@app.route('/login')
def login():

    tw = twitter_api()
    oauth_url, oauth_token, oauth_secret = tw.request_token(request.host_url)
    session['oauth_token'] = oauth_token
    session['oauth_secret'] = oauth_secret
    return redirect(oauth_url)


@app.route('/oauth_callback')
def oauth_login():
    oauth_verifier = request.args.get('oauth_verifier')
    tw = twitter_api()

    oauth_token, oauth_secret = tw.get_oauth_token(
        session['oauth_token'], session['oauth_secret'], oauth_verifier)

    session['oauth_token'] = oauth_token
    session['oauth_secret'] = oauth_secret
    tw.login_twitter_oauth(oauth_token, oauth_secret)

    # アカウント情報取得
    screen_name, profile_image_url = tw.get_account()
    session['screen_name'] = screen_name

    if not os.path.exists('json/' + session['screen_name'] + '.json'):
        with open('json/' + session['screen_name'] + '.json', 'w') as f:
            j = {}
            json.dump(j, f)

    return redirect(url_for('stats'))


@app.route('/logout')
def logout():
    if('oauth_token' in session):
        session.pop('oauth_token', None)
        session.pop('oauth_secret', None)
        session.pop('screen_name', None)
    return redirect(url_for('index'))


@app.route('/add', methods=['POST'])
def add():
    print(request.form)

    shop = request.form['shopName']
    machine = request.form['mName']
    adjust = request.form['adjustment']
    sudden = request.form['suddenValue']
    hidden = request.form['hiddenValue']
    green = request.form['greenValue']

    machine_before = request.form['mName_before'] if 'mName_before' in request.form else None

    with open('json/' + session['screen_name'] + '.json', 'r') as f:
        j = json.load(f)

    if shop not in j:
        j[shop] = {}

    if machine_before is not None:
        j[shop].pop(machine_before)

    j[shop][machine] = {}
    j[shop][machine]['adjust'] = adjust
    j[shop][machine]['sudden'] = sudden
    j[shop][machine]['hidden'] = hidden
    j[shop][machine]['green'] = green

    with open('json/' + session['screen_name'] + '.json', 'w') as f:
        json.dump(j, f)

    return redirect(url_for('stats'))
