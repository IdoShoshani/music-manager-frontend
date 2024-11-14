from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://mongo:27017/music_db")
mongo = PyMongo(app)

# Existing routes remain the same...
@app.route("/api/artists", methods=["GET"])
def get_artists():
    artists = list(mongo.db.artists.find())
    for artist in artists:
        artist["_id"] = str(artist["_id"])
    return jsonify(artists)

@app.route("/api/artists", methods=["POST"])
def add_artist():
    name = request.json.get("name")
    result = mongo.db.artists.insert_one({"name": name, "songs": []})
    return jsonify({
        "success": True,
        "id": str(result.inserted_id)
    })

@app.route("/api/artists/<artist_id>", methods=["DELETE"])
def delete_artist(artist_id):
    mongo.db.artists.delete_one({"_id": ObjectId(artist_id)})
    return jsonify({"success": True})

@app.route("/api/artists/<artist_id>/songs", methods=["POST"])
def add_song(artist_id):
    song = {
        "title": request.json.get("title"),
        "duration": request.json.get("duration")
    }
    mongo.db.artists.update_one(
        {"_id": ObjectId(artist_id)},
        {"$push": {"songs": song}}
    )
    return jsonify({"success": True})

@app.route("/api/artists/<artist_id>/songs/<int:song_index>", methods=["DELETE"])
def delete_song(artist_id, song_index):
    mongo.db.artists.update_one(
        {"_id": ObjectId(artist_id)},
        {"$unset": {f"songs.{song_index}": 1}}
    )
    mongo.db.artists.update_one(
        {"_id": ObjectId(artist_id)},
        {"$pull": {"songs": None}}
    )
    return jsonify({"success": True})

# New routes for playlists
@app.route("/api/playlists", methods=["GET"])
def get_playlists():
    playlists = list(mongo.db.playlists.find())
    for playlist in playlists:
        playlist["_id"] = str(playlist["_id"])
    return jsonify(playlists)

@app.route("/api/playlists", methods=["POST"])
def create_playlist():
    playlist_data = {
        "name": request.json.get("name"),
        "description": request.json.get("description", ""),
        "songs": []
    }
    result = mongo.db.playlists.insert_one(playlist_data)
    return jsonify({
        "success": True,
        "id": str(result.inserted_id)
    })

@app.route("/api/playlists/<playlist_id>", methods=["GET"])
def get_playlist(playlist_id):
    playlist = mongo.db.playlists.find_one({"_id": ObjectId(playlist_id)})
    if playlist:
        playlist["_id"] = str(playlist["_id"])
        return jsonify(playlist)
    return jsonify({"error": "Playlist not found"}), 404

@app.route("/api/playlists/<playlist_id>", methods=["DELETE"])
def delete_playlist(playlist_id):
    mongo.db.playlists.delete_one({"_id": ObjectId(playlist_id)})
    return jsonify({"success": True})

@app.route("/api/playlists/<playlist_id>/songs", methods=["POST"])
def add_song_to_playlist(playlist_id):
    song_data = {
        "artist_id": request.json.get("artist_id"),
        "artist_name": request.json.get("artist_name"),
        "title": request.json.get("title"),
        "duration": request.json.get("duration")
    }
    mongo.db.playlists.update_one(
        {"_id": ObjectId(playlist_id)},
        {"$push": {"songs": song_data}}
    )
    return jsonify({"success": True})

@app.route("/api/playlists/<playlist_id>/songs/<int:song_index>", methods=["DELETE"])
def remove_song_from_playlist(playlist_id, song_index):
    mongo.db.playlists.update_one(
        {"_id": ObjectId(playlist_id)},
        {"$unset": {f"songs.{song_index}": 1}}
    )
    mongo.db.playlists.update_one(
        {"_id": ObjectId(playlist_id)},
        {"$pull": {"songs": None}}
    )
    return jsonify({"success": True})

# New routes for favorites
@app.route("/api/favorites", methods=["GET"])
def get_favorites():
    favorites = mongo.db.favorites.find_one({"type": "user_favorites"}) or {"songs": []}
    if "_id" in favorites:
        favorites["_id"] = str(favorites["_id"])
    return jsonify(favorites)

@app.route("/api/favorites/songs", methods=["POST"])
def add_favorite_song():
    song_data = {
        "artist_id": request.json.get("artist_id"),
        "artist_name": request.json.get("artist_name"),
        "title": request.json.get("title"),
        "duration": request.json.get("duration")
    }
    
    # Initialize favorites document if it doesn't exist
    mongo.db.favorites.update_one(
        {"type": "user_favorites"},
        {
            "$setOnInsert": {"type": "user_favorites", "songs": []},
        },
        upsert=True
    )
    
    # Add the song to favorites if it's not already there
    mongo.db.favorites.update_one(
        {
            "type": "user_favorites",
            "songs": {"$not": {"$elemMatch": {
                "artist_id": song_data["artist_id"],
                "title": song_data["title"]
            }}}
        },
        {"$push": {"songs": song_data}}
    )
    
    return jsonify({"success": True})

@app.route("/api/favorites/songs/<artist_id>/<path:title>", methods=["DELETE"])
def remove_favorite_song(artist_id, title):
    mongo.db.favorites.update_one(
        {"type": "user_favorites"},
        {"$pull": {"songs": {"artist_id": artist_id, "title": title}}}
    )
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)