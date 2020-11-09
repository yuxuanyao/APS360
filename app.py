from flask import Flask, render_template
from music_recommender import MusicRecommender

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def music_recommender():
    # run ml here:
	# mood = model()

    recommender = MusicRecommender("username", "mood")
    playlist_id = recommender.get_playlist()

    return render_template('playlist.html', playlist_id=playlist_id)

if __name__ == "__main__":
	app.run()