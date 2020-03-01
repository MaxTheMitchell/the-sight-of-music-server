import requests,json

URL = "https://api.spotify.com/v1"

AUTHORIZATION_TOKEN = json.load(open('authorization.json'))['authorization_token']

headers  = {
    'Accept' : 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format(AUTHORIZATION_TOKEN)
}