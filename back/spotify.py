import requests,json

URL = "https://api.spotify.com/v1"

class CurrentlyPlaying:

    FAKE_DATA = {
                "item":{
                    "album":{
                        "images": [
                            {"url": 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fi.imgur.com%2FLFhmVaN.jpg&f=1&nofb=1'},
                            {"url": 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fi.imgur.com%2FLFhmVaN.jpg&f=1&nofb=1'},
                            {"url": 'back/nothing_playing'}
                        ]
                    }
                }
            }

    def __init__(self,authorization):
        self.authorization = authorization

    def get_cover64(self):
        return self._get_album()['images'][2]['url']

    def get_cover640(self):
        return self._get_album()['images'][0]['url']

    def _get_album(self):
        return self._get_data()["item"]["album"]

    def _get_data(self):
        try:
            return requests.get(
                url= URL+"/me/player/currently-playing?market=US",
                headers=self.authorization.get_headers()
            ).json()
        except:
            print("No Currrently Playing Song")
            return FAKE_DATA
        
class Search:

    def __init__(self,authorization):
        self.authorization = authorization

    def get_album(self,name):
        return Album(self.authorization,
            self._get_data(name,"album")['albums']['items'][0]['id'])

    def _get_data(self,query,types,limit=1,offset=1):
        return requests.get(
            url= URL+"/search?q={}&type={}&market=US&limit={}&offset={}" \
                .format(query,types,limit,offset),
            headers=self.authorization.get_headers()
        ).json()

class Album:

    def __init__(self,authorization,album_id):
        self.id = album_id
        self.authorization = authorization

    def get_name(self):
        return self._get_data()['name']

    def get_cover64(self):
        return self._get_data()['images'][2]['url']

    def get_cover640(self):
        return self._get_data()['images'][0]['url']
        

    def _get_data(self):
        return requests.get(
            url= URL+"/albums/{}?market=US".format(self.id),
            headers=self.authorization .get_headers()
        ).json()

class Profile:
    
    def __init__(self,authorization):
        self.authorization = authorization

    def _get_data(self):
        return requests.get(
            url= URL+"/v1/me{}".format(self.id),
            headers=self.authorization.get_headers()
        ).json()