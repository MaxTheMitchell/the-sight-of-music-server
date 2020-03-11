import requests,json
import authorization

URL = "https://api.spotify.com/v1"
AUTHORIZATION = authorization.AuthorizationCode()

class CurrentlyPlaying:

    def get_album(self):
        return Album(self._get_data()["item"]["album"]["id"])

    def _get_data(self):
        try:
            return requests.get(
                url= URL+"/me/player/currently-playing?market=US",
                headers=AUTHORIZATION.get_headers()
            ).json()
        except:
            print("No Currrently Playing Song")
            return {}
        
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

    def __init__(self,album_id):
        self.id = album_id

    def get_name(self):
        return self._get_data()['name']

    def get_cover64(self):
        return self._get_data()['images'][2]['url']
        

    def _get_data(self):
        return requests.get(
            url= URL+"/albums/{}?market=US".format(self.id),
            headers=AUTHORIZATION.get_headers()
        ).json()

class Profile:
    AUTHORIZATION = authorization.AuthorizationCode()

    def _get_data(self):
        return requests.get(
            url= URL+"/v1/me{}".format(self.id),
            headers=AUTHORIZATION.get_headers()
        ).json()