import spotipy
import sys
import util

class Recommender:
    def __init__(self, username, mood):
        self.auth_scope = 'user-library-read user-top-read user-follow-read playlist-modify-public'
        self.redirect_uri = 'http://localhost:8888/callback'
        self.client_id = '6bffe904daf84df28e5ec76f6401d2ce'
        self.client_secret = '9d66b726b8f24e1b88d81ac84110495c'
        self.username = username
        self.mood = mood

    def authenticate(self):
        token = spotipy.util.prompt_for_user_token(self.username, self.auth_scope, client_id = self.client_id, 
            client_secret = self.client_secret, redirect_uri = self.redirect_uri)
        
        if token:
            self.sp = spotipy.Spotify(auth=token)
        else:
            raise Exception("Authentication failure")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        mood = sys.argv[2]
    else:
        sys.exit()

    recommender = Recommender(username, mood)
    recommender.authenticate()