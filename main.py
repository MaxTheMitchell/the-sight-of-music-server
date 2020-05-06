import flask,os,json
from back.authorization import AuthorizationCode
from back.spotify import CurrentlyPlaying
from back.image_analysis import ImageAnalyser
app = flask.Flask(__name__)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
PORT = os.getenv("PORT")
REDIRECT_URI = os.getenv("REDIRECT_URI")+"/authorize/code"

auth = AuthorizationCode(CLIENT_ID,CLIENT_SECRET,REDIRECT_URI,'user-read-currently-playing')
current_song = CurrentlyPlaying(auth)

@app.route('/')
def main():
    if auth.is_fully_initalized():
        return (open("front/main.html","rb").read()+ \
             bytes("<h1>Currently Playing:\n</h1><img src={}>".format(
                 current_song.get_cover640()),'utf-8'))
    return flask.redirect('/authorize')

@app.route('/authorize')
def authorize():
    return flask.redirect(auth.get_login_url())

@app.route('/authorize/login')
def login():
    return flask.redirect(auth.get_login_url(True))

@app.route('/authorize/code')
def make_tokens():
    auth.make_tokens(flask.request.args.get('code', None))
    return flask.redirect('/')

@app.route('/image/pixles')
def get_pixles_in_album():
    return str(ImageAnalyser(current_song.get_cover64()).get_pixles())

@app.route('/image/pixles/<numb>')
def get_numb_pixles(numb):
    return str(ImageAnalyser(current_song.get_cover64()).get_pixles(int(numb)))

@app.route('/image/pixles/<numb>/section')
def get_section(numb):
    return str(ImageAnalyser(current_song.get_cover64()).get_subsection_of_pixles(
        int(numb),
        int(flask.request.args.get('start', None)),
        int(flask.request.args.get('end', None))
    ))

@app.route('/image/display/<resolution>')
def get_image_at_resolution(resolution):
    resolution = int(resolution)
    if resolution < 64:
        img = current_song.get_cover64()
    elif resolution < 300:
        img = current_song.get_cover300()
    else:
        return "{} is an invalid resolution".format(resolution)
    return ImageAnalyser(img).get_html_askii_display(resolution)


app.run(host="0.0.0.0",port=PORT)
