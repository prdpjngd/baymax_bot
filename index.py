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
        seprate_chat=chat_history.spit("%227%")
        for i in seprate_chat:
            analysis=TextBlob(i)
            sentiment_solo=sentiment_solo+analysis.sentiment.polarity

        sentiments=sentiment_solo/length(seprate_chat)
        #spotipy-setup
        client_id="bb592cc71fbf46ba83c57b311f9e0c7d"
        client_secret="74fa7053d85449bcadc234693b065821"
        client_credentials_manager=SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        result=sp.search("Happier")
        url=result["tracks"]["items"][0]["artists"][0]["external_urls"]["spotify"]

        genres=''
        ans=''
        if sentiments <= -.1 and sentiments > -.2:
            ans="I think you should listen folk ,\n Here is the link:"+url
            genres='roots'
        elif sentiments >=.1 and sentiments <.2:
            ans="I think you should listen chill ,\n Here is the link:"+url
            genres='chill'
        elif sentiments >=.2 and sentiments <.3:
            ans="I think you should listen indian ,\n Here is the link:"+url
            genres='indian'
        elif sentiments <=-.2 and sentiments >-.3:
            ans="I think you should listen classical ,\n Here is the link:"+url
            genres='classical'
        elif sentiments >=.6 and sentiments <.8:
            ans="I think you should listen dance ,\n Here is the link:"+url
            genres='party'
        elif sentiments <=-.6 and sentiments >-.8:
            ans="I think you should listen romance ,\n Here is the link:"+url
            genres='romance'
        elif sentiments >=.4 and sentiments <.6:
            ans="I think you should listen happy ,\n Here is the link:"+url
            genres='happy'
        elif sentiments <.4 and sentiments >=.3:
            ans="I think you should listen hip-hop ,\n Here is the link:"+url
            genres='hip-hop'
        elif sentiments >=.8 and sentiments <1.0:
            ans="I think you should listen disco music ,\n Here is the link:"+url
            genres='disco'
        elif sentiments >-0.1 and sentiments <=0.1:
            ans="I think you should listen dubstep music,\n Here is the link:"+url
            genres='dubstep'


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
