from app import app, SM
from flask import redirect, render_template, request, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
import users
from fileinput import filename
from song_manager import SongManager
from datetime import datetime

@app.route('/uploads/<path:filename>')
def send_upload(filename):
    filename = f"{filename}.mp3"
    return send_from_directory('uploads', filename)

@app.route("/listen/<song_id>")
def listen(song_id):
    song_info = SM.getinfo(song_id)
    if song_info != -1:
        return render_template("song.html", song = song_id, song_artist = song_info[0], song_name = song_info[1], song_genre = song_info[2], song_duration = song_info[3])
    else:
        return render_template("error.html", message="Oops no song")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if not users.login(username, password):
        return render_template("error.html", message="Wrong username or password!")
    return redirect("/")

@app.route("/logout")
def logout():
    del session["user_name"]
    return redirect("/")

@app.route("/profile/<user_id>", methods=["get"])
def profile(user_id):
    p_artistname = users.artist(user_id)
    user_songs = SM.get_songs(user_id)
    return render_template("profile.html", p_artistname = p_artistname, user_songs = user_songs, p_id = user_id)


@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Username too short or long! (1-20 characters)")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="The passwords aren't matching!")
        if password1 == "":
            return render_template("error.html", message="The password is empty!")

        artist_name = request.form["artist_name"]
        if len(artist_name) > 100:
            return render_template("error.html", message="Artist name too long! (max 100 characters)")
        elif len(artist_name) == 0:
            artist_name = username

        if users.register(username, artist_name, password1) == False:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        return redirect("/")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    return render_template("upload.html")

@app.route("/submit", methods=["POST"])
def submit():
    song = request.files['song']
    song_data = song.read()  # Read the song data into memory
    name = request.form['song_name']
    genre = request.form['genre']
    duration = SM.calcduration(song_data)
    if genre == "Custom":
        genre = request.form['custom_genre']
    timestamp = datetime.now()
    if SM.save_song(song_data, name, genre, duration, timestamp):
        return render_template("success.html")
    else:
        return render_template("error.html", message="An oopsie woopsie happened with saving the song")