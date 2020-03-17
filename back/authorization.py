import requests,json,base64,time,flask

class ClientCredentials:

    def __init__(self):
        with open('back/authorization.json') as auth:
            authorization = json.load(auth)
            self.CLIENT_ID = authorization['client_id']
            self.CLIENT_SECRET = authorization['client_secret']
        self._refresh_auth_token()
        self.token_type = "Bearer"

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

    def __init__(self,cleint_id,client_secret,redirect_uri,scope=''):
        self.access_token = ''
        self.token_type = 'Bearer'
        self.expriation = 0
        self.refresh_token = ''
        self.scope = scope
        self.REDIRECT_URI = redirect_uri
        self.CLIENT_ID = cleint_id
        self.CLIENT_SECRET = client_secret

    def get_headers(self):
        self._handle_tokens()
        return {
            'Accept' : 'application/json',
            'Content-Type': 'application/json',
            'Authorization': '{} {}'.format(self.token_type,self.access_token)
            }
        
    def is_fully_initalized(self):
        return self.refresh_token != ''

    def get_login_url(self):
        return """
            https://accounts.spotify.com/authorize?
            client_id={}
            &response_type=code
            &redirect_uri={}
            &scope={}
            """.format(self.CLIENT_ID,self.REDIRECT_URI,self.scope
                ).replace("\n",'').replace(" ","")

    def make_tokens(self,code): 
        data = self._access_api_token({
                    "grant_type" : 'authorization_code',
                    "code" : code,
                    "redirect_uri" : self.REDIRECT_URI
                })
        self.access_token, self.token_type, expiration_time_span, self.refresh_token, self.scope = data.values()
        self._update_expriation(expiration_time_span)

    def login_workflow(self):
        print("Go to this url and athorize:\n")
        print(self._get_login_url())
        self._make_tokens(input("\nenter code in redirected url:\n").strip().replace("\n",''))


    def _handle_tokens(self):
        if self._is_expired():
            if self._no_access_token():
                self._login_workflow()
            else:
                self._refresh_access_token()

    def _no_access_token(self):
        return self.access_token == ''

    def _is_expired(self):
        return self.expriation <= time.time()

    def _update_expriation(self,time_span):
        self.expriation = int(time.time()+int(time_span))


    def _refresh_access_token(self):
        self.access_token, self.token_type, expiration_time_span, self.scope = \
            self._access_api_token({
                "grant_type" : 'refresh_token',
                "refresh_token": self.refresh_token
            })
        self._update_expriation(expiration_time_span)

    def _access_api_token(self,data):
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
                    data=data
                ).json()
        