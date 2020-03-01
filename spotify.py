import requests,json,base64

URL = "https://api.spotify.com/v1"

with open('authorization.json') as authorization:
    authorization = json.load(authorization)
    CLIENT_ID = authorization['client_id']
    CLIENT_SECRET = authorization['client_secret']

headers  = {
    'Accept' : 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format("foo")
}

def get_auth_token():
    return requests.post(
        url="https://accounts.spotify.com/api/token",
        headers={
            "Authorization" : "Basic {}" \
                .format(
                    base64.b64encode(
                        (CLIENT_ID+':'+CLIENT_SECRET).encode()
                    ).decode("utf-8")
                )
        },
        data={
            "grant_type" : 'client_credentials'
        }
    )

class CurrentlyPlaying:

    def get_album(self):
        return self._get_data()["item"]["album"]

    def _get_data(self):
        return requests.get(
            url= URL+"/me/player/currently-playing",
            headers=headers
        ).json()
        