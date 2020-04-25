import requests
import base64
import json,string,random
import nltk
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from  textblob import TextBlob
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
            #else-end-here
        r=requests.get('https://console.dialogflow.com/api-client/demo/embedded/86f65547-dbee-4b4a-ae30-28d6b297f137/demoQuery', headers=headers, params=params).text
        j=json.loads(r)

        sentiment_solo=0
        f = open("./sessions/"+s_id,"r")
        chat_history=f.read()
        f.close()
        seprate_chat=chat_history.split("%227%")
        for i in seprate_chat:
            analysis=TextBlob(i)
            sentiment_solo=sentiment_solo+analysis.sentiment.polarity

        sentiments=sentiment_solo/len(seprate_chat)
        genres=''
        ans=''
        if sentiments <= -.1 and sentiments > -.2:
            url="https://open.spotify.com/playlist/3pr1uTmByJcCqcfUHNNDQa"
            genres='roots'
        elif sentiments >=.1 and sentiments <.2:
            url="https://open.spotify.com/playlist/37i9dQZF1DX889U0CL85jj"
            genres='chill'
        elif sentiments >=.2 and sentiments <.3:
            url="https://open.spotify.com/playlist/1EO12soyEcN8KPfTqyqkxY"
        elif sentiments <=-.2 and sentiments >-.3:
            url="https://open.spotify.com/playlist/6an0hNyshVMWORG7qVNUbq"
        elif sentiments >=.6 and sentiments <.8:
            url="https://open.spotify.com/playlist/2jAQlUjsDn0FrdECMLFdrF"
            genres='party'
        elif sentiments <=-.6 and sentiments >-.8:
            url="https://open.spotify.com/playlist/1oSlx4XxBp12uknXcuhaDg"
            genres='romance'
        elif sentiments >=.4 and sentiments <.6:
            url="https://open.spotify.com/playlist/4kE5mLoJMWBwQjx0jKzIFJ"
            genres='happy'
        elif sentiments <.4 and sentiments >=.3:
            url="https://open.spotify.com/playlist/0wOMJ3Hs0KVvKbGUNOlmo1"
            genres='hip-hop'
        elif sentiments >=.8 and sentiments <1.0:
            url="https://open.spotify.com/playlist/2jAQlUjsDn0FrdECMLFdrF"
            genres='disco'
        elif sentiments >-0.1 and sentiments <=0.1:
            url="https://open.spotify.com/playlist/3ObJ6Qra3CkV0gNCRTtK0c"
            genres='dubstep'
        url=url.replace("https://open.spotify.com/","https://open.spotify.com/embed/")
        ans=ans+'<iframe src="'+url+'" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'
        return str(ans)+'<br>'+j['result']['fulfillment']['speech']+'sentiment :'+str(sentiments)
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
