import flask,os
from back.authorization import AuthorizationCode
app = flask.Flask(__name__)

auth = AuthorizationCode('user-read-currently-playing')

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
def main():
    return open("front/main.html","rb").read()

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.getenv("PORT"))