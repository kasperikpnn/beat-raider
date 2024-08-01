import os
from db import db
from flask import abort, request, session
from sqlalchemy import text
import users
import song_manager
from app import SM
from datetime import datetime 

def initSetup():
    if users.whois(1) != "Neotride":
        users.register_admin("neotride", "Neotride", "1234")
        print("Neotride registered")
        users.register("testi", "testi", "1234")
        print("testi registered")
        try:
            bliss = open("sample_songs/bliss.mp3", "rb")
            dreams = open("sample_songs/dreams.mp3", "rb")
            sorry = open("sample_songs/sorry.mp3", "rb")
            print("Sample songs loaded")
        except:
            print("Sample songs not loaded!")
        timestamp = datetime.now()
        SM.save_song(1, bliss.read(), "Bliss", "Electronic", 210, timestamp)
        SM.save_song(1, dreams.read(), "Dreams", "Electronic", 224, timestamp)
        SM.save_song(1, sorry.read(), "Sorry (Outro)", "Electronic", 144, timestamp)
        print("Initial users and songs added")

