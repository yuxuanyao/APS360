import spotipy
import sys
import random

class MusicRecommender:
    def __init__(self, username, mood):
        self.auth_scope = 'user-library-read user-top-read user-follow-read playlist-modify-public'
        self.redirect_uri = 'http://localhost:8888/callback'
        self.client_id = '6bffe904daf84df28e5ec76f6401d2ce'
        self.client_secret = '9d66b726b8f24e1b88d81ac84110495c'
        self.username = username
        self.mood_to_music_type = {
            0: "Calm",
            1: "Calm",
            2: "Calm",
            3: "None",
            4: "Cheerful",
            5: "Calm",
            6: "None"
        }
        self.music_type = self.mood_to_music_type[int(mood)]

    def authenticate(self):
        token = spotipy.util.prompt_for_user_token(self.username, self.auth_scope, client_id = self.client_id, 
            client_secret = self.client_secret, redirect_uri = self.redirect_uri)
        
        if token:
            self.sp = spotipy.Spotify(auth=token)
        else:
            raise Exception("Authentication failure")
    
    def get_top_tracks(self):
        top_tracks_uri = []
        top_artists_data = self.sp.current_user_top_artists(limit=50, time_range="long_term")
        top_artists = top_artists_data['items']

        for top_aritist in top_artists:
            top_artists_uri = top_aritist['uri']
            top_tracks_data = self.sp.artist_top_tracks(top_artists_uri)
            top_tracks = top_tracks_data['tracks']
            for top_track in top_tracks:
                top_tracks_uri.append(top_track['uri'])
        
        return top_tracks_uri
    
    def get_mood_tracks(self):
        mood_tracks_uri = []
        top_tracks = self.get_top_tracks()
        top_tracks_batch = [top_tracks[i:i+50] for i in range(0, len(top_tracks), 50)]

        for batch in top_tracks_batch:
            top_tracks_data = self.sp.audio_features(batch)
            for track in top_tracks_data:
                if self.music_type == "Calm":
                    if (0.25 <= track["valence"] <= 0.5
                    and track["danceability"] <= 0.25
                    and track["energy"] <= 0.25):
                        mood_tracks_uri.append(track["uri"])
                elif self.music_type == "Cheerful":
                    if (0.75 <= track["valence"] <= 1
                    and track["danceability"] <= 0.75
                    and track["energy"] <= 0.75):
                        mood_tracks_uri.append(track["uri"])

        return mood_tracks_uri	
    
    def get_playlist(self):
        if self.music_type == "None":
            return
        
        self.authenticate()

        user_data = self.sp.current_user()
        user_id = user_data["id"]
        
        playlist = self.sp.user_playlist_create(user_id, "Driving Music: " + self.music_type)
        playlist_id = playlist["id"]

        mood_tracks = self.get_mood_tracks()
        random.shuffle(mood_tracks)
        self.sp.user_playlist_add_tracks(user_id, playlist_id, mood_tracks[:50])

        return playlist_id
		
if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        mood = sys.argv[2]
    else:
        print("Usage: python music_recommender.py <username> <mood>")
        sys.exit()

    recommender = MusicRecommender(username, mood)
    playlist_id = recommender.get_playlist()
    print(playlist_id)