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

## Current status

The user can:
- log in and out, and create a new account
- when registering, they can set a separate "artist name" from their username
- upload music formatted as .mp3 on the platform (saved in the /uploads folder of the app)
- check out their profile page, displaying all of the music they have uploaded
- edit their artist name, change their password, set their profile description
- create playlists
- add songs to a playlist
- edit their songs: includes editing the genre, the song name, the song description (work-in-progress)
- delete their songs

The songs:
- have a set title and genre by the artist
- can be listened to either from the user's profile page, or from a separate individual page
- have an unique ID consisting of 10 Base64 characters: this is necessary so that the songs can be uploaded on the server without them accidentally sharing names
- can be interacted with using a simple audio player I made in JavaScript
- have a timestamp for when they were uploaded, which is shown in a "humanized" way on the website (ex. "2 minutes ago")

Playlists:
- work in progress!
- can be created: they have a name and an upload date
- you can add songs in them
- amount of songs is counted
- can't be listened to, or deleted yet

UI:

- implemented layout.html which is extended to almost every template. displays the text BeatRaider which just simply takes you to front page, for easier navigation

To-do:

Users:
- commenting and liking
- adding admin users: ability to delete all songs, edit all profiles and song information
- possibly basic profile pictures? choose from a set of ASCII pictures
- ability to delete playlists

Songs:
- will have descriptions
- implement likes and (possibly depending on time) play count on songs

Front page:
- will have songs on it, probably just the most recent songs
- will have a search bar!!! search for songs with a specific name, genre, songs that were uploaded this week/today...

Security:
- passwords saved in plain text currently. need to save them in hash
- browser cache may cause some issues security-wise later (I've been logged in as users that shouldn't exist anymore)

UI:
- will be as much in text as possible, no images, or even buttons! this is by design, and will probably make things harder for me. (it was already hard making the seek bar in text) why? i just like the idea of it. will include ASCII art possibly to make it look better

If there's extra time:
- implement BPM for songs (not automatic, will be filled by the artist). can be used for searching songs with a specific BPM