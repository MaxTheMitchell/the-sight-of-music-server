import spotify
import time


cp = spotify.CurrentlyPlaying()
search = spotify.Search()

while 1:
    time.sleep(2)
    print(cp.get_album().get_name())