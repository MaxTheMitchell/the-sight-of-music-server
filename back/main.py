from back import spotify,authorization
# print(spotify.Search()._get_data())
# print(spotify.CurrentlyPlaying()._get_data())

print(authorization.AuthorizationCode()._user_login())