# BeatRaider

BeatRaider is an audio uploading and streaming service, most similar to SoundCloud.

## How to start the app locally

- clone this repository
- create a file called `.env` in the root of the folder, containing these lines:
```
DATABASE_URL=<your database here>
SECRET_KEY=<your secret key here>
```
- activate the virtual environment and install the required libraries with the commands:
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```
- now set the schema of the database with the command:
```
psql < schema.sql
```
- and finally, boot the app with the command
```
flask run
```

## Final status

The user can:
- log in and out, and create a new account
- when registering, they can set a separate "artist name" from their username
- upload music formatted as .mp3 on the platform (saved in the /uploads folder of the app)
- check out their profile page, displaying all of the music they have uploaded and playlists they have created
- edit their artist name, change their password, set their profile description
- create playlists
- add songs to a playlist
- edit their songs: includes editing the genre, the song name, the song description
- delete their songs
- comment on songs
- can be admin, being able to edit and delete all songs, comments, playlists, profile descriptions etc. only restricted to the user "neotride", password is 1234

The songs:
- have a set title and genre by the artist
- can be listened to either from the user's profile page, or from a separate individual page
- have an unique ID consisting of 10 Base64 characters: this is necessary so that the songs can be uploaded on the server without them accidentally sharing names
- can be interacted with using a simple audio player I made in JavaScript
- have a timestamp for when they were uploaded, which is shown in a "humanized" way on the website (ex. "2 minutes ago")

Playlists:
- can be created: they have a name and an upload date
- you can add songs in them
- amount of songs is counted
- functions as a "selection of songs": had no time to implement listening to all of the playlist at once, shuffle, etc
- can't actually remove songs from playlists, didn't have time to implement this either

UI:
- implemented layout.html which is extended to almost every template
- implemented CSS. Almost all buttons are text on purpose, for the "early Internet" aesthetic
  
Security:
- only the hash values of passwords are saved
- accounts for CSRF vulnerability

## Notes for testing

- the admin username is ``neotride`` and password is ``1234``
- other users have been created for testing, such as ``anamanaguchi``, ``kevinmcleod``, and ``porterrobinson``. All of their passwords are ``1234``
- songs have been added on the web site for search/pagination/etc testing purposes. All of the songs used are fair use, and were officially available for free download. (Songs under Neotride are songs I have personally made)
