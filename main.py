import flask,os,json
from back.authorization import AuthorizationCode
app = flask.Flask(__name__)

# with open('back/authorization.json') as auth:
#     authorization = json.load(auth)
#     CLIENT_ID = authorization['client_id']
#     CLIENT_SECRET = authorization['client_secret']
#     REDIRECT_URI = authorization['redirect_uri']

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "https://localhost:8080/authorize/code/"

auth = AuthorizationCode(CLIENT_ID,CLIENT_SECRET,REDIRECT_URI,'user-read-currently-playing')


@app.route('/')
def main():
    return open("front/main.html","rb").read()

@app.route('/authorize')
def authorize():
    return flask.redirect(auth._get_login_url())

@app.route('/authorize/code/?code=<code>')
def make_tokens(code):
    print(code)
    auth._make_tokens(code)
    return flask.redirect('/')



# app.run(host="localhost",port="8080")
app.run(host="0.0.0.0",port=os.getenv("PORT"))