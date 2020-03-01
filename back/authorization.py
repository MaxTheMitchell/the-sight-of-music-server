import requests,json,base64,time


class ClientCredentials:

    def __init__(self):
        with open('back/authorization.json') as auth:
            authorization = json.load(auth)
            self.CLIENT_ID = authorization['client_id']
            self.CLIENT_SECRET = authorization['client_secret']
        self._refresh_auth_token()

    def get_headers(self):
        return  {
        'Accept' : 'application/json',
        'Content-Type': 'application/json',
        'Authorization': '{} {}'.format(self.token_type,self._get_auth_token())
        }

    def _get_auth_token(self):
        if self._token_is_expired():
           self._refresh_auth_token()
        return self.auth_token

    def _token_is_expired(self):
        return self.refresh_time <= time.clock()

    def _refresh_auth_token(self):
        response = self._make_auth_token_req()
        self.refresh_time = time.clock()+response['expires_in']
        self.token_type = response['token_type']
        self.auth_token = response['access_token']

    def _make_auth_token_req(self):
        return requests.post(
            url="https://accounts.spotify.com/api/token",
            headers={
                "Authorization" : "Basic {}" \
                    .format(
                        base64.b64encode(
                            (self.CLIENT_ID+':'+self.CLIENT_SECRET).encode()
                        ).decode("utf-8")
                    )
            },
            data={
                "grant_type" : 'client_credentials'
            }
        ).json()

class AuthorizationCode:

    def __init__(self):
        with open('authorization.json') as auth:
            authorization = json.load(auth)
            self.CLIENT_ID = authorization['client_id']
            self.CLIENT_SECRET = authorization['client_secret']

    def _user_login(self):
        return requests.get(
            url="https://accounts.spotify.com/authorize"
        ).json()
