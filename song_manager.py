import os
import random
from sqlalchemy import text
from flask import abort, request, session
from db import db
import idgen
from tempfile import gettempdir
import users
from mutagen.mp3 import MP3
import datetime as dt
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

class SongManager:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)

    def calcduration(self, song_data):
        # Write the song data to a temporary file to calculate its duration
        temp_dir = gettempdir()
        temp_path = os.path.join(temp_dir, 'temp_song.mp3')
        with open(temp_path, 'wb') as f:
            f.write(song_data)
        audio = MP3(temp_path)
        duration = int(audio.info.length)
        
        # Clean up the temporary file
        os.remove(temp_path)
        return duration

    def save_song(self, user_id, song_data, name, genre, duration, timestamp):
        duration = str(timedelta(seconds=duration))
        id = idgen.generate_id()
        filename = f"{id}.mp3"
        file_path = os.path.join(self.upload_folder, filename)
        if isinstance(song_data, str):
            song_data = song_data.encode()
        with open(file_path, 'wb') as f:
            f.write(song_data)
        sql = text("INSERT INTO songs (id, user_id, name, genre, duration, timestamp) VALUES (:id, :user_id, :name, :genre, :duration, :timestamp)")
        db.session.execute(sql, {"id":id, "user_id":user_id, "name":name, "genre":genre, "duration":duration, "timestamp":timestamp})
        db.session.commit()
        return True

    def delete_song(self, song_id):
        self.delete_song_file(song_id)
        sql = text("DELETE FROM playlist_songs WHERE song_id = :song_id")
        db.session.execute(sql, {"song_id":song_id})
        db.session.commit()
        sql = text("DELETE FROM liked_songs WHERE song_id = :song_id")
        db.session.execute(sql, {"song_id":song_id})
        db.session.commit()
        sql = text("DELETE FROM comments WHERE song_id = :song_id")
        db.session.execute(sql, {"song_id":song_id})
        db.session.commit()
        sql = text("DELETE FROM songs WHERE id = :song_id")
        db.session.execute(sql, {"song_id":song_id})
        db.session.commit()
        return True

    def delete_playlist(self, playlist_id):
        sql = text("DELETE FROM playlist_songs WHERE playlist_id = :playlist_id")
        db.session.execute(sql, {"song_id":playlist_id})
        db.session.commit()
        sql = text("DELETE FROM playlists WHERE id = :playlist_id")
        db.session.execute(sql, {"id":playlist_id})
        db.session.commit()
        return True

    def save_playlist(self, user_id, name):
        timestamp = dt.datetime.now()
        sql = text("INSERT INTO playlists (user_id, name, timestamp) VALUES (:user_id, :name, :timestamp)")
        db.session.execute(sql, {"user_id":user_id, "name":name, "timestamp":timestamp})
        db.session.commit()
        return True

    def countSongsOnPlaylist(self, playlist_id):
        sql = text("SELECT COUNT(*) FROM playlist_songs WHERE playlist_id = :playlist_id")
        result = db.session.execute(sql, {"playlist_id":playlist_id})
        count = result.scalar()
        return count

    def getinfo(self, song_id):
        sql = text("SELECT id, user_id, name, genre, duration, likes, playcount, timestamp, description FROM songs WHERE id = :song_id")
        result = db.session.execute(sql, {"song_id":song_id})
        song = result.fetchone()
        if not song:
            print("No song found") ## Debugging
            return -1
        print(song)
        print("Song found") ## Debugging
        return [users.artist(song[1]), song[2], song[3], song[4], song[5], song[6], song[7], song[0], song[1], song[8]]
        ## artist name, song name, genre, duration, likes, playcount, timestamp, song ID, user ID, description

    def update_song_info(self, song_id, delete_confirm, new_songname, new_desc, new_genre):
        if delete_confirm == "Y":
            self.delete_song(song_id)
            return True
        else:
            if new_songname:
                self.update_songname(song_id, new_songname)
            if new_desc:
                self.update_song_desc(song_id, new_desc)
            if new_genre:
                self.update_song_genre(song_id, new_genre)
            return True


    def update_songname(self, song_id, new_songname):
        try:
            sql = text("UPDATE songs SET name=:new_songname WHERE id=:song_id")
            db.session.execute(sql, {"new_songname":new_songname, "song_id":song_id})
            db.session.commit()
        except:
            return False
        return True

    def update_song_desc(self, song_id, new_desc):
        try:
            sql = text("UPDATE songs SET description=:new_desc WHERE id=:song_id")
            db.session.execute(sql, {"new_desc":new_desc, "song_id":song_id})
            db.session.commit()
        except:
            return False
        return True

    def update_song_genre(self, song_id, new_genre):
        try:
            sql = text("UPDATE songs SET genre=:new_genre WHERE id=:song_id")
            db.session.execute(sql, {"new_genre":new_genre, "song_id":song_id})
            db.session.commit()
        except:
            return False
        return True

    def update_playlist_info(self, playlist_id, delete_confirm, new_playlistname):
        if delete_confirm == "Y":
            self.delete_playlist(playlist_id)
            return True
        else:
            if new_playlistname:
                self.update_playlistname(playlist_id, new_playlistname)
            return True

    def update_playlistname(self, playlist_id, new_playlistname):
        try:
            sql = text("UPDATE playlists SET name=:new_playlistname WHERE id=:playlist_id")
            db.session.execute(sql, {"new_playlistname":new_playlistname, "playlist_id":playlist_id})
            db.session.commit()
        except:
            return False
        return True

    def getPlaylistInfo(self, playlist_id):
        sql = text("SELECT id, user_id, name, timestamp FROM playlists WHERE id = :playlist_id")
        result = db.session.execute(sql, {"playlist_id":playlist_id})
        playlist = result.fetchone()
        if not playlist:
            return []
        songCount = self.countSongsOnPlaylist(playlist_id)
        return [playlist[0], users.artist(playlist[1]), playlist[1], playlist[2], playlist[3], songCount]
        ## playlist id, artist name of the creator of playlist, id of the creator of playlist, name of playlist, timestamp, song count

    def delete_song_file(self, filename):
        file_path = os.path.join(self.upload_folder, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    def edit_song(self, old_filename, new_file):
        if self.delete_song(old_filename):
            return self.save_song(new_file)
        return None

    def get_songs(self, user_id):
        sql = text("SELECT id FROM songs WHERE user_id = :user_id")
        result = db.session.execute(sql, {"user_id":user_id})
        songs = []
        if result:
            for song in result:
                songs.append(SongManager.getinfo(self, song.id))
        print(songs)
        return songs
    
    def get_playlists(self, user_id):
        sql = text("SELECT id FROM playlists WHERE user_id = :user_id ORDER BY timestamp")
        result = db.session.execute(sql, {"user_id":user_id})
        playlists = []
        if result:
            for playlist in result:
                playlists.append(SongManager.getPlaylistInfo(self, playlist.id))
        return playlists

    def get_random_songs(self, limit):
        sql = text("SELECT id FROM songs ORDER BY RANDOM() LIMIT :limit")
        result = db.session.execute(sql, {"limit":limit})
        songs = []
        if result:
            for song in result:
                songs.append(SongManager.getinfo(self, song.id))
        print(songs)
        return songs
    
    def song_to_playlist(self, playlist_id, song_id):
        try:
            # Insert the song into the playlist
            sql = text("INSERT INTO playlist_songs (playlist_id, song_id) VALUES (:playlist_id, :song_id)")
            db.session.execute(sql, {"playlist_id": playlist_id, "song_id": song_id})
            db.session.commit()
            
        except IntegrityError as e:
            db.session.rollback()  # Roll back the session to maintain consistency
            if 'duplicate key value violates unique constraint' in str(e):
                raise UniqueViolation('The song is already in the selected playlist.')
            else:
                raise e  # Re-raise other integrity errors
        return True

    def get_recent_songs(self, limit, offset=0):
        # Retrieve songs with limit and offset for pagination
        sql = text("SELECT id FROM songs ORDER BY timestamp DESC LIMIT :limit OFFSET :offset")

        result = db.session.execute(sql, {"limit": limit, "offset": offset})
        songs = []
        
        if result:
            for song in result:
                songs.append(SongManager.getinfo(self, song.id))
        
        print(songs)
        return songs
    
    def total_songs(self):
        sql = text("SELECT COUNT(*) FROM songs")
        result = db.session.execute(sql)
        if result:
            return result.scalar()
        else:
            return 0