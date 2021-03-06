import spotipy
import sys
import random

class MusicRecommender:
    def __init__(self, token, mood):
        self.token = token
        self.mood_to_music_type = {
            0: "Calm",
            1: "Calm",
            2: "None",
            3: "Cheerful",
            4: "Calm",
            5: "None"        
        }
        self.music_type = self.mood_to_music_type[int(mood)]

    def authenticate(self):
        if self.token:
            self.sp = spotipy.Spotify(auth=self.token)
        else:
            raise Exception("Authentication failure")
    
    def get_top_artists(self):
        top_artists_name = set()
        top_artists_uri = []
        top_artists_data = self.sp.current_user_top_artists(limit=50, time_range="long_term")
        top_artists = top_artists_data["items"]

        for top_aritist in top_artists:
            top_artists_name.add(top_aritist["name"])
            top_artists_uri.append(top_aritist["uri"])
            related_artist_data = self.sp.artist_related_artists(top_aritist["uri"])
            related_artists = related_artist_data["artists"][:4]
            for related_artist in related_artists:
                if related_artist["name"] not in top_artists_name:
                    top_artists_name.add(related_artist["name"])
                    top_artists_uri.append(related_artist["uri"])

        return top_artists_uri

    def get_top_tracks(self):
        top_tracks_uri = []
        top_artists = self.get_top_artists()
        
        for top_artist in top_artists:
            top_tracks_data = self.sp.artist_top_tracks(top_artist)
            top_tracks = top_tracks_data["tracks"]
            for top_track in top_tracks:
                top_tracks_uri.append(top_track["uri"])

        return top_tracks_uri
    
    def get_mood_tracks(self):
        mood_tracks_uri = []
        top_tracks = self.get_top_tracks()
        top_tracks_batch = [top_tracks[i:i+100] for i in range(0, len(top_tracks), 100)]

        for batch in top_tracks_batch:
            top_tracks_data = self.sp.audio_features(batch)
            for track in top_tracks_data:
                if self.music_type == "Calm":
                    if (0.25 <= track["valence"] <= 0.75
                    and track["danceability"] <= 0.5
                    and track["energy"] <= 0.5):
                        mood_tracks_uri.append(track["uri"])
                elif self.music_type == "Cheerful":
                    if (0.75 <= track["valence"] <= 1
                    and track["danceability"] >= 0.7
                    and track["energy"] >= 0.7):
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