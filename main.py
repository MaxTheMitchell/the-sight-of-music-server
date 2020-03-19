import flask,os,json
from back.authorization import AuthorizationCode
from back.spotify import CurrentlyPlaying
app = flask.Flask(__name__)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
REDIRECT_URI = os.getenv("REDIRECT_URI")+"/authorize/code"

auth = AuthorizationCode(CLIENT_ID,CLIENT_SECRET,REDIRECT_URI,'user-read-currently-playing')
current_song = CurrentlyPlaying(auth)

@app.route('/')
def main():
    if auth.is_fully_initalized():
        return open("front/main.html","rb").read() +\
             bytes("<img src={}>".format(
                 current_song.get_album().get_cover640()),'utf-8')
    return open("front/main.html","rb").read()
    # return flask.redirect('/authorize')

@app.route('/authorize')
def authorize():
    return flask.redirect(auth.get_login_url())

@app.route('/authorize/code')
def make_tokens():
    auth.make_tokens(flask.request.args.get('code', None))
    return flask.redirect('/')

app.run(host="0.0.0.0",port=PORT)
