import os
from sqlalchemy import text
from flask import abort, request, session
from db import db
import idgen
import users
from mutagen.mp3 import MP3

class SongManager:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)

    def calcduration(self, song_data):
        # Write the song data to a temporary file to calculate its duration
        temp_path = os.path.join('temp', 'temp_song.mp3')
        with open(temp_path, 'wb') as f:
            f.write(song_data)
        audio = MP3(temp_path)
        duration = int(audio.info.length)
        
        # Clean up the temporary file
        os.remove(temp_path)
        return duration

    def save_song(self, song_data, name, genre, duration, timestamp):
        id = idgen.generate_id()
        filename = f"{id}.mp3"
        file_path = os.path.join(self.upload_folder, filename)
        with open(file_path, 'wb') as f:
            f.write(song_data)
        sql = text("INSERT INTO songs (id, user_id, name, genre, duration, timestamp) VALUES (:id, :user_id, :name, :genre, :duration, :timestamp)")
        db.session.execute(sql, {"id":id, "user_id":session["user_id"], "name":name, "genre":genre, "duration":duration, "timestamp":timestamp})
        db.session.commit()
        return True

    def getinfo(self, song_id):
        sql = text("SELECT id, user_id, name, genre, duration, likes, playcount, timestamp FROM songs WHERE id = :song_id")
        result = db.session.execute(sql, {"song_id":song_id})
        song = result.fetchone()
        if not song:
            print("No song found")
            return -1
        print(song)
        print("Song found")
        return [users.artist(song[1]), song[2], song[3], song[4], song[5], song[6], song[7], song[0]]
        ## artist name, song name, genre, duration, likes, playcount, timestamp, song ID

    def delete_song(self, filename):
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