from flask import Flask, render_template, request, redirect, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:5000/api")

@app.route("/health")
def health_check():
    # Checks the health of the frontend
    return {"status": "healthy"}, 200

@app.route("/")
def index():
    # Fetch all required data
    artists_response = requests.get(f"{BACKEND_URL}/artists")
    playlists_response = requests.get(f"{BACKEND_URL}/playlists")
    favorites_response = requests.get(f"{BACKEND_URL}/favorites")
    
    return render_template(
        "index.html",
        artists=artists_response.json(),
        playlists=playlists_response.json(),
        favorites=favorites_response.json().get("songs", [])
    )

# Existing artist routes...
@app.route("/artist", methods=["POST"])
def add_artist():
    name = request.form.get("name")
    requests.post(f"{BACKEND_URL}/artists", json={"name": name})
    return redirect(url_for("index"))

@app.route("/artist/<artist_id>/delete", methods=["POST"])
def delete_artist(artist_id):
    requests.delete(f"{BACKEND_URL}/artists/{artist_id}")
    return redirect(url_for("index"))

@app.route("/artist/<artist_id>/song", methods=["POST"])
def add_song(artist_id):
    song_data = {
        "title": request.form.get("title"),
        "duration": request.form.get("duration")
    }
    requests.post(f"{BACKEND_URL}/artists/{artist_id}/songs", json=song_data)
    return redirect(url_for("index"))

@app.route("/artist/<artist_id>/song/<int:song_index>/delete", methods=["POST"])
def delete_song(artist_id, song_index):
    requests.delete(f"{BACKEND_URL}/artists/{artist_id}/songs/{song_index}")
    return redirect(url_for("index"))

# Playlist routes
@app.route("/playlist", methods=["POST"])
def create_playlist():
    playlist_data = {
        "name": request.form.get("name"),
        "description": request.form.get("description", "")
    }
    requests.post(f"{BACKEND_URL}/playlists", json=playlist_data)
    return redirect(url_for("index"))

@app.route("/playlist/<playlist_id>/delete", methods=["POST"])
def delete_playlist(playlist_id):
    requests.delete(f"{BACKEND_URL}/playlists/{playlist_id}")
    return redirect(url_for("index"))

@app.route("/playlist/<playlist_id>/song", methods=["POST"])
def add_song_to_playlist(playlist_id):
    artist_id = request.form.get("artist_id")
    artist_name = request.form.get("artist_name")
    song_data = {
        "artist_id": artist_id,
        "artist_name": artist_name,
        "title": request.form.get("title"),
        "duration": request.form.get("duration")
    }
    requests.post(f"{BACKEND_URL}/playlists/{playlist_id}/songs", json=song_data)
    return redirect(url_for("index"))

@app.route("/playlist/<playlist_id>/song/<int:song_index>/delete", methods=["POST"])
def remove_song_from_playlist(playlist_id, song_index):
    requests.delete(f"{BACKEND_URL}/playlists/{playlist_id}/songs/{song_index}")
    return redirect(url_for("index"))

# Favorites routes
@app.route("/favorites/song", methods=["POST"])
def add_to_favorites():
    song_data = {
        "artist_id": request.form.get("artist_id"),
        "artist_name": request.form.get("artist_name"),
        "title": request.form.get("title"),
        "duration": request.form.get("duration")
    }
    requests.post(f"{BACKEND_URL}/favorites/songs", json=song_data)
    return redirect(url_for("index"))

@app.route("/favorites/song/<artist_id>/<path:title>/delete", methods=["POST"])
def remove_from_favorites(artist_id, title):
    requests.delete(f"{BACKEND_URL}/favorites/songs/{artist_id}/{title}")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)