import requests
import ast
import urllib.parse
import base64
import os
import json
from flask import Flask, render_template, request, redirect, make_response
app = Flask(__name__)


#how to get environment varible values -->  " os.environ['S3_KEY'] "

@app.route('/bot',methods = ['GET'])
def df():
    q = request.args.get('q')
    s_id='gyut872638o'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
    }

    params = (
        ('q', q),
        ('sessionId', s_id),
    )

    r=requests.get('https://console.dialogflow.com/api-client/demo/embedded/86f65547-dbee-4b4a-ae30-28d6b297f137/demoQuery', headers=headers, params=params).text
    j=json.loads(r)
    return j['result']['fulfillment']['speech']


@app.route('/',methods = ['GET'])
def home():
    return render_template('index.html')

@app.route('/login',methods = ['GET'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
