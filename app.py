import os
from flask import Flask, render_template, flash, request
from music_recommender import MusicRecommender
from werkzeug.utils import secure_filename
from model import preprocess, predict

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def music_recommender():
    valid = False
    if "username" not in request.form or "file" not in request.files:
        flash("No file or form part")
    username = request.form["username"]
    file = request.files["file"]
    if username == "" or file.filename == "":
        flash("Missing username or file")
    if file and allowed_file(file.filename):
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
        
        recommender = MusicRecommender(username, result)
        playlist_id = recommender.get_playlist()
        return render_template("playlist.html", playlist_id=playlist_id)
    
    # invalid, alert message

if __name__ == "__main__":
	app.run()