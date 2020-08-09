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
img_url = ""

@app.route('/')
def main():
    if auth.is_fully_initalized():
        return (
            bytes("<script>let ownImg = {}</script>".format(str(img_url != "").lower()),'utf-8')+
            open("front/main.html","rb").read()+ \
             bytes("<h1>Currently Playing:\n</h1><img class='main_img' src={}>".format(
                #  current_song.get_cover640()
                get_img(False)
                 ),'utf-8'))
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
    return str(ImageAnalyser( get_img()).get_pixles())

@app.route('/image/pixles/<numb>')
def get_numb_pixles(numb):
    return str(ImageAnalyser( get_img()).get_pixles(int(numb)))

@app.route('/image/pixles/<numb>/section')
def get_section(numb):
    return str(ImageAnalyser( get_img()).get_subsection_of_pixles(
        int(numb),
        int(flask.request.args.get('start', None)),
        int(flask.request.args.get('end', None)),
        bool(flask.request.args.get('format565',False))
    ))

@app.route('/image/pixles/<numb>/section/reversed')
def get_reversed_section(numb):
    return str(ImageAnalyser( get_img()).get_half_reversed_subsection_of_pixles(
        int(numb),
        int(flask.request.args.get('start', None)),
        int(flask.request.args.get('end', None))
    ))

@app.route('/image/display/<resolution>')
def get_image_at_resolution(resolution):
    resolution = int(resolution)
    if resolution < 64:
        img =  get_img()
    elif resolution < 300:
        img =  get_img(False)
    else:
        return "{} is an invalid resolution".format(resolution)
    return ImageAnalyser(img).get_html_askii_display(resolution)

@app.route('/image/set')
def set_img_url():
    global img_url
    img_url = flask.request.args.get('img_url', default = "")
    return bytes(img_url,'utf-8')

def get_img(sixty_four=True):
    global img_url
    if img_url != "" and img_url != "null":
        return img_url
    elif sixty_four:
        return current_song.get_cover64()
    return current_song.get_cover640()

app.run(host="0.0.0.0",port=PORT)
