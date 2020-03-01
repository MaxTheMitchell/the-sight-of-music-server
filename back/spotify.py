import requests,json
import authorization

URL = "https://api.spotify.com/v1"
AUTHORIZATION = authorization.ClientCredentials()

class CurrentlyPlaying:

    def get_album(self):
        return self._get_data()["item"]["album"]

    def _get_data(self):
        return requests.get(
            url= URL+"/me/player/currently-playing",
            headers=AUTHORIZATION.get_headers()
        ).json()
        
class Search:

    def get_album(self,name):
        return Album(self._get_data(name,"album")['albums']['items'][0]['id'])

    def _get_data(self,query,types,limit=1,offset=1):
        return requests.get(
            url= URL+"/search?q={}&type={}&market=US&limit={}&offset={}" \
                .format(query,types,limit,offset),
            headers=AUTHORIZATION.get_headers()
        ).json()

class Album:

    def __init__(self,id):
        self.id = id

    def get_cover64(self):
        return self._get_data()['images'][2]['url']
        

    def _get_data(self):
        return requests.get(
            url= URL+"/albums/{}".format(self.id),
            headers=AUTHORIZATION.get_headers()
        ).json()