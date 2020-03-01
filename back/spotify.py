import requests,json
from back import authorization

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



    def _get_data(self):
        return requests.get(
            url= URL+"/search?q=Untrue&type=album&market=US&limit=1&offset=5",
            headers=AUTHORIZATION.get_headers()
        ).json()