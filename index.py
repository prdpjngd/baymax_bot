import requests
import base64
import json,string,random
from flask import Flask, render_template, request, redirect, make_response, session,url_for
app = Flask(__name__)
app.secret_key = '767rgdb263tr'

#how to get environment varible values -->  " os.environ['S3_KEY'] "

@app.route('/bot',methods = ['GET'])
def df():
    q = request.args.get('q')
    s_id = request.args.get('s_id')
    if s_id :
        f = open("./sessions/"+s_id,"a+")
        if 'logout' in q:
            session.pop('uname', None)
            return "see you ... you'r logged out"
        else:
            f.write(q+"%227%")
            f.close()
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
    else:
        return "{Error:True,Type:Invalid Session ID,Code:507},"


@app.route('/',methods = ['GET'])
def home():
    if 'uname' in session:
        username = session['uname']
        return render_template('index.html',username=username)
    else:
        return redirect(url_for('login'))

@app.route('/login',methods = ['GET'])
def login():
    uname = request.args.get('username')
    passwd = request.args.get('password')
    N = 7
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
    if(len(str(uname))==0 or len(str(passwd))==0):
        return "{Error:True,Type:Empty-U/P,Code:509}"
    elif uname and passwd:
        session['uname'] = uname
        return redirect(url_for('home',token=res))
    else:
        return render_template('login.html')

@app.route('/logout',methods = ['GET'])
def logout():
    session.pop('uname', None)
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)
