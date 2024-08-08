from app import app, SM
from flask import jsonify, redirect, render_template, request, send_from_directory, session
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

@app.route("/edit_profile/<user_id>",methods=["GET", "POST"])
def edit_profile(user_id):
    if request.method == "GET":
        p_artistname = users.artist(user_id)
        p_desc = users.desc(user_id)
        return render_template("edit_profile.html", p_artistname = p_artistname, p_desc = p_desc, p_id = user_id)
    if request.method == "POST":
        new_artistname = request.form["artist_name"]
        new_desc = request.form["desc"]
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        new_password2 = request.form["new_password2"]
        error = users.update_information(user_id, new_artistname, new_desc, old_password, new_password, new_password2)
        if not error:
            return profile(user_id)
        else:
            return render_template("error.html", message=error)


@app.route("/listen/<song_id>")
def listen(song_id):
    song_info = SM.getinfo(song_id)
    if song_info != -1:
        return render_template("song.html", song = song_id, song_artist = song_info[0], song_name = song_info[1], song_genre = song_info[2], song_duration = song_info[3])
    else:
        return render_template("error.html", message="Oops no song")

@app.route('/load_more_songs', methods=['GET', 'POST'])
def load_more_songs():
    limit = 5  # Number of songs to load each time
    offset = request.form.get('offset', default=0, type=int)
    
    # Determine if the request is for going back
    direction = request.form.get('direction')
    if direction == 'back':
        offset = max(0, offset - (2 * limit))  # Go back by the limit amount, ensuring it doesn't go below 0

    # Get recent songs
    recent_songs = SM.get_recent_songs(limit, offset)
    
    # Get the total number of songs
    total_songs = SM.total_songs()  # You will need to implement this method

    # Check if there are no more songs to load
    no_more_songs = len(recent_songs) == 0

    return render_template('index.html', 
                           recent_songs=recent_songs, 
                           offset=offset + limit,  # Update offset for the next load
                           no_more_songs=no_more_songs,
                           total_songs=total_songs)  # Pass total songs to template

@app.route("/")
def index():
    recent_songs = SM.get_recent_songs(5)
    total_songs = SM.total_songs()
    for song in recent_songs:
        print(song[3])
        print(isinstance(song[3], int))
    return render_template("index.html", recent_songs = recent_songs, total_songs = total_songs, offset=0)

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
    return render_template("profile.html", p_artistname = p_artistname, user_songs = user_songs, p_id = int(user_id), p_desc = users.desc(user_id))


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
    if SM.save_song(session["user_id"], song_data, name, genre, duration, timestamp):
        return render_template("success.html")
    else:
        return render_template("error.html", message="An oopsie woopsie happened with saving the song")