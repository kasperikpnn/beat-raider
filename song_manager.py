import os
from sqlalchemy import text
from flask import abort, request, session
from db import db
import idgen
import users

class SongManager:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)

    def save_song(self, song_file, name, genre, timestamp):
        id = idgen.generate_id()
        filename = f"{id}.mp3"
        file_path = os.path.join(self.upload_folder, filename)
        song_file.save(file_path)
        sql = text("INSERT INTO songs (id, user_id, name, genre, timestamp) VALUES (:id, :user_id, :name, :genre, :timestamp)")
        db.session.execute(sql, {"id":id, "user_id":session["user_id"], "name":name, "genre":genre, "timestamp":timestamp})
        db.session.commit()
        return True

    def getinfo(self, song_id):
        sql = text("SELECT id, user_id, name, genre, timestamp FROM songs WHERE id = :song_id")
        result = db.session.execute(sql, {"song_id":song_id})
        song = result.fetchone()
        if not song:
            print("No song found")
            return -1
        print(song)
        print("Song found")
        return [users.whois(song[1]), song[2], song[3], song[4], song[0]]

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