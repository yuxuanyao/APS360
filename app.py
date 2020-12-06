import os
from flask import Flask, render_template, request, redirect, url_for
from music_recommender import MusicRecommender
from werkzeug.utils import secure_filename
from model import preprocess, predict
import startup

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("auth.html") 

@app.route("/", methods=["POST"])
def auth():
    response = startup.getUser()
    return redirect(response)

@app.route('/callback/')
def callback():
    startup.getUserToken(request.args['code'])
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template("index.html") 

@app.route("/home", methods=["POST"])
def music_recommender():
    valid = False
    file = request.files["file"]
    if file.filename != "" and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        valid = True
    
    if valid:
        # preprocess image
        tensor = preprocess(filepath)
        # run model:
        result = predict(tensor)
        # delete uploaded image
        os.remove(filepath)

        token, _, _, _ = startup.getAccessToken()
        recommender = MusicRecommender(token, result)
        playlist_id = recommender.get_playlist()
        if playlist_id is None:
            return redirect(url_for('no_music'))
        return redirect(url_for('result', playlist_id=playlist_id))
    
    # invalid, alert message

@app.route('/result/<playlist_id>/')
def result(playlist_id):
    return render_template("playlist.html", playlist_id=playlist_id)

@app.route('/no_music')
def no_music():
    return render_template("no_music.html")

if __name__ == "__main__":
    app.run()