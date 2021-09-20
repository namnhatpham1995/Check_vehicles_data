# File to route the web app to appropriate address
import flask
from MainApp import app
from flask import render_template, redirect, url_for, flash, request
import base64
import requests
from urllib.parse import urlparse

id = ""
secret = ""
API_URL = 'https://api.mercedes-benz.com/experimental/connectedvehicle/v2/vehicles'
AUTH_URL = 'https://id.mercedes-benz.com/as/authorization.oauth2'
TOKEN_URL = 'https://id.mercedes-benz.com/as/token.oauth2'
TRY_URL = 'https://api.mercedes-benz.com/experimental/connectedvehicle_tryout/v2/vehicles'


# Default page
@app.route('/')
@app.route('/index')
def index():
    code = flask.request.args.get("code")
    if code is not None:
        print(code)
        return redirect(url_for('get_token', code=code))
    else:
        return redirect(url_for('login'))


# Page to insert ID and Secret key
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if not request.form['username'] and not request.form['password']:  # Check if the log in form is not filled
            flash('Please enter username and password!', 'error')
        else:
            global id
            global secret
            id = request.form['username']  # take user's identity from input
            secret = request.form['password']
            print(id)
            print(secret)
            return redirect(url_for('get_auth_code'))
    return render_template('login.html')


# Get authentication code used for getting token
@app.route('/get_auth_code', methods=['GET', 'POST'])
def get_auth_code():
    print(id)
    host = urlparse(request.base_url)
    redirect_uri = "http://" + host.hostname
    url = AUTH_URL + "?response_type=code&redirect_uri=" + redirect_uri + ":5000/&client_id=" + id + "&scope=mb:vehicle:status:general mb:user:pool:reader offline_access "
    return redirect(url)


# Get token
@app.route('/get_token/<code>', methods=['GET', 'POST'])
def get_token(code):
    Encoded_ID_Secret = (base64.b64encode((id + ":" + secret).encode("ascii"))).decode("ascii")

    headers = {
        'Authorization': 'Basic ' + Encoded_ID_Secret,
        'content-type': 'application/x-www-form-urlencoded',
    }

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://192.168.0.126:5000/'
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    # contentType = response.headers.get("content-type")
    # print(contentType)
    response_json = response.json()
    global access_token
    global refresh_token
    access_token = response_json['access_token']
    print("Access_Token: " + access_token)
    print(type(access_token))
    refresh_token = response_json['refresh_token']
    print("Refresh_Token: " + refresh_token)
    #return redirect(url_for('try_out'))
    return redirect(url_for('call_api'))
    #return response.content


# Call API using token
@app.route('/call_api', methods=['GET', 'POST'])
def call_api():
    try:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            "authorization": "Bearer " + access_token
        }

    except:
        print('No available token')
    print(headers)
    response = requests.get(API_URL, headers=headers)
    response_json = response.json()
    error_code = response_json['code']
    return response.content


# Test demo
@app.route('/try_out', methods=['GET', 'POST'])
def try_out():
    try:
        headers = {
            "authorization": "Bearer " + "a1b2c3d4-a1b2-a1b2-a1b2-a1b2c3d4e5f6"
        }
        print(headers)
    except:
        print('No available token')

    response = requests.get(TRY_URL, headers=headers)
    response_json = response.json()
    # error_code = response_json['code']
    return response.content
