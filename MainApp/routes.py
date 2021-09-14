# File to route the web app to appropriate address
import flask
from MainApp import app
from flask import render_template, redirect, url_for
import base64
import requests


# Main route to check json request
@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    url = "https://id.mercedes-benz.com/as/authorization.oauth2?response_type=code&redirect_uri=http://192.168.0.126:5000/&client_id=e9d578af-58ee-4615-a60b-7c8db464c05f&scope=mb:vehicle:status:general mb:user:pool:reader offline_access"
    return redirect(url)


@app.route('/get_token/<code>', methods=['GET', 'POST'])
def get_token(code):
    ID = "e9d578af-58ee-4615-a60b-7c8db464c05f"
    Secret = "MEZmOIEuZivXjjrSvqfFDnJrFrUoKkOlcYzxRetszvKYqjOlhOXeHWYwfDISCSIk"
    Encoded_ID_Secret = (base64.b64encode((ID + ":" + Secret).encode("ascii"))).decode("ascii")

    headers = {
        'Authorization': 'Basic ' + Encoded_ID_Secret,
        'content-type': 'application/x-www-form-urlencoded',
    }

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://192.168.0.126:5000/'
    }

    response = requests.post('https://id.mercedes-benz.com/as/token.oauth2', headers=headers, data=data)
    # contentType = response.headers.get("content-type")
    # print(contentType)
    response_json = response.json()
    print(response_json['access_token'])
    return response.content


@app.route('/')
@app.route('/index')
def index():
    code = flask.request.args.get("code")
    if code is not None:
        print(code)
        return redirect(url_for('get_token', code=code))
    else:
        return render_template("mainPage.html")
