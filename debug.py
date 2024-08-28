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
        users.register("anamanaguchi", "Anamanaguchi", "1234")
        users.register("kevinmcleod", "Kevin MacLeod", "1234")
        users.register("porterrobinson", "Porter Robinson", "1234")
        print("testi registered")
        try:
            bliss = open("sample_songs/bliss.mp3", "rb")
            dreams = open("sample_songs/dreams.mp3", "rb")
            sorry = open("sample_songs/sorry.mp3", "rb")
            sting_operation = open("sample_songs/sting_operation.mp3", "rb")
            helix_nebula = open("sample_songs/helix_nebula.mp3", "rb")  
            airbase = open("sample_songs/airbase.mp3", "rb")
            video_challenge = open("sample_songs/video_challenge.mp3", "rb")
            fast_turtle = open("sample_songs/fast_turtle.mp3", "rb")
            flora_fauna = open("sample_songs/flora_fauna.mp3", "rb")
            power_supply = open("sample_songs/power_supply.mp3", "rb")
            canon = open("sample_songs/canon.mp3", "rb")
            danse = open("sample_songs/danse.mp3", "rb")
            endless = open("sample_songs/endless.mp3", "rb")
            ghost = open("sample_songs/ghost.mp3", "rb")
            sinfonia = open("sample_songs/sinfonia.mp3", "rb")
            hollowheart = open("sample_songs/hollowheart.mp3", "rb")
            she = open("sample_songs/she.mp3", "rb")
            print("Sample songs loaded")
        except:
            print("Sample songs not loaded!")
        timestamp = datetime.now()

        # Neotride songs
        SM.save_song(1, bliss.read(), "Bliss", "Electronic", 210, timestamp)
        SM.save_song(1, dreams.read(), "Dreams", "Electronic", 224, timestamp)
        SM.save_song(1, sorry.read(), "Sorry (Outro)", "Electronic", 144, timestamp)

        # Anamanaguchi songs
        sting_operation_content = sting_operation.read()
        SM.save_song(2, sting_operation_content, "Sting Operation", "Electronic", SM.calcduration(sting_operation_content), timestamp)

        helix_nebula_content = helix_nebula.read()
        SM.save_song(2, helix_nebula_content, "Helix Nebula", "Electronic", SM.calcduration(helix_nebula_content), timestamp)

        airbase_content = airbase.read()
        SM.save_song(2, airbase_content, "Airbase", "Electronic", SM.calcduration(airbase_content), timestamp)

        video_challenge_content = video_challenge.read()
        SM.save_song(2, video_challenge_content, "Video Challenge", "Electronic", SM.calcduration(video_challenge_content), timestamp)

        fast_turtle_content = fast_turtle.read()
        SM.save_song(2, fast_turtle_content, "Fast Turtle", "Electronic", SM.calcduration(fast_turtle_content), timestamp)

        flora_fauna_content = flora_fauna.read()
        SM.save_song(2, flora_fauna_content, "Flora/Fauna", "Electronic", SM.calcduration(flora_fauna_content), timestamp)

        power_supply_content = power_supply.read()
        SM.save_song(2, power_supply_content, "Power Supply", "Electronic", SM.calcduration(power_supply_content), timestamp)

        # Kevin MacLeod songs
        canon_content = canon.read()
        SM.save_song(3, canon_content, "Canon in D Major", "Classical", SM.calcduration(canon_content), timestamp)

        danse_content = danse.read()
        SM.save_song(3, danse_content, "Danse Macabre", "Classical", SM.calcduration(danse_content), timestamp)

        endless_content = endless.read()
        SM.save_song(3, endless_content, "The Endless", "Classical", SM.calcduration(endless_content), timestamp)

        ghost_content = ghost.read()
        SM.save_song(3, ghost_content, "Ghost Dance", "Classical", SM.calcduration(ghost_content), timestamp)

        sinfonia_content = sinfonia.read()
        SM.save_song(3, sinfonia_content, "Sinfonia Number 5", "Classical", SM.calcduration(sinfonia_content), timestamp)

        # Porter Robinson songs
        hollowheart_content = hollowheart.read()
        SM.save_song(4, hollowheart_content, "Hollowheart", "Electronic", SM.calcduration(hollowheart_content), timestamp)

        she_content = she.read()
        SM.save_song(4, she_content, "She Heals Everything", "Electronic", SM.calcduration(she_content), timestamp)

        print("Initial users and songs added")

