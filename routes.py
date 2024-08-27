from app import app, SM
from flask import jsonify, abort, get_flashed_messages, redirect, render_template, request, send_from_directory, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
import users
from fileinput import filename
from song_manager import SongManager
from datetime import datetime
from psycopg2.errors import UniqueViolation
from mutagen.mp3 import MP3
from mutagen import MutagenError

@app.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    playlist_id = request.form.get('playlist_id')
    song_id = request.form.get('song_id')
    next_url = request.form.get('next', url_for('profile', user_id=session['user_id']))
    
    if not playlist_id or not song_id:
        flash('Playlist ID and Song ID are required.', 'error')
        return redirect(next_url)

    try:
        SM.song_to_playlist(playlist_id, song_id)
        flash('Song added to playlist successfully!', 'success')
    except UniqueViolation:
        flash('The song is already in the selected playlist.', 'error')
    except Exception as e:
        flash(f'Failed to add song to playlist: {str(e)}', 'error')

    return redirect(next_url)

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    playlistCount = SM.total_user_playlists(session["user_id"])
    if playlistCount == 10:
        flash('Maximum amount of playlists already created (10)!', 'error')
        return redirect(url_for('profile', user_id=session["user_id"]))
    playlist_user_id = session["user_id"]
    playlist_name = request.form.get('playlistName')
    if playlist_name:
        if users.validate(playlist_user_id):
            if SM.save_playlist(playlist_user_id, playlist_name):
                flash('Playlist created successfully!', 'success')
    else:
        flash('Playlist name is required.', 'error')
    
    return redirect(url_for('profile', user_id=session["user_id"]))  # Redirect back to the profile page

@app.route('/uploads/<path:filename>')
def send_upload(filename):
    filename = f"{filename}.mp3"
    return send_from_directory('uploads', filename)

@app.route("/edit_profile/<user_id>",methods=["GET", "POST"])
def edit_profile(user_id):
    if request.method == "GET":
        if users.user_id_exists(user_id):
            if str(user_id) == str(session["user_id"]) or session.get("is_admin"):
                p_artistname = users.artist(user_id)
                p_desc = users.desc(user_id)
                next_url = request.referrer or url_for('profile', user_id=session['user_id'])
                return render_template("edit_profile.html", p_artistname = p_artistname, p_desc = p_desc, p_id = user_id, next_url = next_url)
            else:
                flash("You don't have the permission to edit this user's profile!", 'error')
                return redirect("/")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        new_artistname = request.form["artist_name"]
        new_desc = request.form["desc"]
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        new_password2 = request.form["new_password2"]
        next_url = request.form.get('next', url_for('profile', user_id=session['user_id']))
        error = users.update_information(user_id, new_artistname, new_desc, old_password, new_password, new_password2)
        if error == True:
            return redirect(next_url)
        else:
            flash('Something went wrong with updating the information! You likely tried to change the password but they did not match.', 'error')
            return redirect(next_url)

@app.route("/edit/<song_id>",methods=["GET", "POST"])
def edit(song_id):
    if request.method == "GET":
        song_info = SM.getinfo(song_id)
        if song_info != -1:
            if song_info[8] == session["user_id"] or session.get("is_admin"):
                next_url = request.referrer or url_for('profile', user_id=session['user_id'])
                return render_template("edit.html", song = song_info, next_url = next_url)
            else:
                flash("You don't have the permission to edit this song!", 'error')
                return redirect("/")
        else:
            existing_messages = get_flashed_messages(with_categories=True)
            specific_message_exists = any(category == 'success' and message == 'Successfully deleted the song!' for category, message in existing_messages)
            if not specific_message_exists:
                flash(f'A song with provided ID does not exist!', 'error')
            return redirect("/")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        delete_confirm = request.form.get('delete_confirm', '')
        new_songname = request.form.get('song_name', '')
        new_desc = request.form.get('desc', '')
        new_genre = request.form.get('genre', '')
        next_url = request.form.get('next', url_for('profile', user_id=session['user_id']))
        if new_genre == "Custom":
            new_genre = request.form.get('custom_genre', '')
        print(f"delete_confirm: {delete_confirm}, new_songname: {new_songname}, new_desc: {new_desc}, new_genre: {new_genre}, song_id: {song_id}")
        try:
            SM.update_song_info(song_id, delete_confirm, new_songname, new_desc, new_genre)
            if delete_confirm == "Y":
                flash('Successfully deleted the song!', 'success')
                next_url = url_for('profile', user_id=session['user_id'])
            else:
                flash('Successfully updated the song information!', 'success')
        except Exception as e:
            flash(f'Failed to edit the song: {str(e)}', 'error')

    return redirect(next_url)

@app.route("/editplaylist/<playlist_id>",methods=["GET", "POST"])
def editplaylist(playlist_id):
    if request.method == "GET":
        playlist_info = SM.getPlaylistInfo(playlist_id)
        if playlist_info:
            if str(playlist_info[2]) == session["user_id"] or session.get("is_admin"):
                next_url = request.referrer or url_for('profile', user_id=session['user_id'])
                return render_template("editplaylist.html", playlist = playlist_info, next_url = next_url)
            else:
                flash("You don't have the permission to edit this playlist!", 'error')
                return redirect("/")
        else:
            flash(f'A playlist with provided ID does not exist!', 'error')
            return redirect("/")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        delete_confirm = request.form.get('delete_confirm', '')
        new_playlistname = request.form.get('playlist_name', '')
        next_url = request.form.get('next', url_for('profile', user_id=session['user_id']))
        try:
            SM.update_playlist_info(playlist_id, delete_confirm, new_playlistname)
            if delete_confirm == "Y":
                flash('Successfully deleted the playlist!', 'success')
                next_url = "/" # Takes the user back to front page if deleted
            else:
                flash('Successfully updated the playlist information!', 'success')
        except Exception as e:
            flash(f'Failed to edit the playlist: {str(e)}', 'error')

    return redirect(next_url)


@app.route("/listen/<song_id>")
def listen(song_id):
    song_info = SM.getinfo(song_id)
    user_playlists = []
    if session.get("logged_in") == True:
        user_playlists = SM.get_playlists(session["user_id"])
    if song_info != -1:
        return render_template("song.html", user_playlists = user_playlists, song = song_id, song_artist = song_info[0], song_name = song_info[1], song_genre = song_info[2], song_duration = song_info[3], song_timestamp = song_info[6], song_user_id = song_info[8], song_description = song_info[9])
    else:
        flash('Song not found with this ID! Oopsie!', 'error')
        return redirect("/")

@app.route('/search', methods=["GET"])
def search():
    name = request.args.get('name', '')
    genre = request.args.get('genre', '')
    time = request.args.get('time', 'all_time')
    limit = 5  # Number of songs to display per page
    offset = request.args.get('offset', default=0, type=int)

    # Fetch search results with pagination
    search_results = SM.search_for_songs(name=name, genre=genre, time=time, limit=limit, offset=offset)
    
    # Fetch the total number of results for pagination
    total_results = SM.total_search_results(name=name, genre=genre, time=time)

    no_more_results = False
    if total_results == 0:
        flash('No songs found!', 'error')
    else:
        no_more_results = offset + limit >= total_results

    return render_template('search.html', 
                           search_results=search_results, 
                           name=name, 
                           genre=genre, 
                           time=time,
                           offset=offset, 
                           no_more_results=no_more_results,
                           total_results=total_results,
                           limit=limit)

@app.route('/load_more_songs', methods=['POST'])
def load_more_songs():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    limit = 5  # Number of songs to load each time
    offset = request.form.get('offset', default=0, type=int)
    next_url = request.form.get('next_url')
    
    # Determine if the request is for going back
    direction = request.form.get('direction')
    if direction == 'back':
        offset = max(0, offset - limit)  # Go back by the limit amount, ensuring it doesn't go below 0
    else:
        offset += limit  # Move forward by the limit amount

    # Get recent songs with pagination
    recent_songs = SM.get_recent_songs(limit, offset)
    
    # Get the total number of songs
    total_songs = SM.total_songs()

    # Check if there are no more songs to load
    no_more_songs = offset + limit >= total_songs

    return render_template(next_url, 
                           recent_songs=recent_songs, 
                           offset=offset,  # Update offset for the next load
                           no_more_songs=no_more_songs,
                           total_songs=total_songs,
                           limit=limit)  # Pass limit to template

@app.route('/load_more_user_songs', methods=['POST'])
def load_more_user_songs():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    limit = 5  # Number of songs to load each time
    offset = request.form.get('offset', default=0, type=int)
    next_url = request.form.get('next_url')
    user_id = request.form.get('user_id')
    p_artistname = users.artist(user_id)
    user_playlists = []
    if session.get("logged_in") == True:
        user_playlists = SM.get_playlists(session["user_id"])
    artist_playlists = SM.get_playlists(user_id)
    # Determine if the request is for going back
    direction = request.form.get('direction')
    if direction == 'back':
        offset = max(0, offset - limit)  # Go back by the limit amount, ensuring it doesn't go below 0
    else:
        offset += limit  # Move forward by the limit amount

    user_songs = SM.get_songs(user_id, limit, offset)
    
    # Get the total number of songs
    total_songs = SM.total_user_songs(user_id)

    # Check if there are no more songs to load
    no_more_songs = offset + limit >= total_songs

    return render_template(next_url, 
                           user_songs=user_songs, 
                           offset=offset,  # Update offset for the next load
                           no_more_songs=no_more_songs,
                           total_songs=total_songs,
                           p_artistname = p_artistname,
                           user_playlists=user_playlists,
                           artist_playlists=artist_playlists,
                           p_id = int(user_id),
                           p_desc = users.desc(user_id),
                           limit=limit)  # Pass limit to template

@app.route("/")
def index():
    limit = 5
    recent_songs = SM.get_recent_songs(limit)
    total_songs = SM.total_songs()
    user_playlists = []
    if session.get("logged_in") == True:
        user_playlists = SM.get_playlists(session["user_id"])
    for song in recent_songs:
        print(song[3])
        print(isinstance(song[3], int))
    return render_template("index.html", user_playlists = user_playlists, recent_songs = recent_songs, total_songs = total_songs, offset=0, limit = limit)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if not users.login(username, password):
        flash('Wrong username or password!', 'error')
    return redirect("/")

@app.route("/logout")
def logout():
    del session["user_name"]
    del session["user_id"]
    del session["csrf_token"]
    del session["logged_in"]
    return redirect("/")

@app.route("/profile/<user_id>", methods=["get"])
def profile(user_id):
    if users.user_id_exists(user_id):
        limit = 5
        p_artistname = users.artist(user_id)
        total_songs = SM.total_user_songs(user_id)
        user_songs = SM.get_songs(user_id, limit)
        user_playlists = []
        if session.get("logged_in") == True:
            user_playlists = SM.get_playlists(session["user_id"])
        artist_playlists = SM.get_playlists(user_id)
        return render_template("profile.html", p_artistname = p_artistname, user_songs = user_songs, total_songs = total_songs, user_playlists = user_playlists, artist_playlists = artist_playlists, p_id = int(user_id), p_desc = users.desc(user_id), offset=0, limit = limit)
    else:
        flash('User does not exist!', 'error')
        return redirect("/")

@app.route("/playlist/<playlist_id>", methods=["get"])
def playlist(playlist_id):
    limit = 5
    playlist_info = SM.getPlaylistInfo(playlist_id)
    total_songs = SM.total_songs()
    playlist_songs = SM.get_playlist_songs(playlist_id)
    user_playlists = []
    if session.get("logged_in") == True:
        user_playlists = SM.get_playlists(session["user_id"])
    return render_template("playlist.html", playlist = playlist_info, playlist_songs = playlist_songs, total_songs = total_songs, user_playlists = user_playlists, offset=0, limit = limit)   

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            flash('The username is too short or too long! (max 20 characters)', 'error')
            return redirect("/register")

        if users.user_exists(username):
            flash('This username is already in use!', 'error')
            return redirect("/register")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            flash('The passwords are not matching!', 'error')
            return redirect("/register")
        if password1 == "":
            flash('The password is empty!', 'error')
            return redirect("/register")

        artist_name = request.form["artist_name"]
        if len(artist_name) > 100:
            flash('The artist name is too long! (max 100 characters)!', 'error')
            return redirect("/register")
        elif len(artist_name) == 0:
            artist_name = username

        if users.register(username, artist_name, password1) == False:
            flash('Registration unsuccessful for an unknown reason', 'error')
            return redirect("/")
        flash('Registration successful!', 'success')
        users.login(username, password1)
        return redirect("/")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if session.get("logged_in") == True:
        return render_template("upload.html")
    else:
        flash('Uploading allowed only for users!', 'error')
        return redirect("/")

@app.route("/submit", methods=["POST"])
def submit():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    song = request.files['song']
    song_data = song.read()  # Read the song data into memory
    try:
        mp3_file = MP3(song)
    except MutagenError:
        flash('The uploaded file is not a valid MP3.', 'error')
        return redirect("/upload")
    name = request.form['song_name']
    genre = request.form['genre']
    duration = SM.calcduration(song_data)
    if genre == "Custom":
        genre = request.form['custom_genre']
    timestamp = datetime.now()
    try:
        SM.save_song(session["user_id"], song_data, name, genre, duration, timestamp)
        flash('Successfully uploaded the song!!', 'success')
    except Exception as e:
        flash(f'Failed to upload the song: {str(e)}', 'error')
    return redirect("/profile/" + str(session["user_id"]))