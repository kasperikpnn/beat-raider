# BeatRaider

BeatRaider is an audio uploading and streaming service, most similar to SoundCloud.

## How to start the app locally

- clone this repository
- create a file called `.env` in the root of the folder, containing these lines:
```
DATABASE_URL=postgresql://testi:1234@localhost:5432/mydatabase
SECRET_KEY=95d3763bb55e744e77dd181a47b4e1c6
```
- activate the virtual environment and install the required libraries with the commands:
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```
- now set the schema of the database with the commands:
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

The songs:
- have a set title and genre by the artist
- can be listened to either from the user's profile page, or from a separate individual page
- have an unique ID consisting of 10 Base64 characters: this is necessary so that the songs can be uploaded on the server without them accidentally sharing names
- can be interacted with using a simple audio player I made in JavaScript

To-do:

Users:
- profile description
- editing artist name
- make, edit and delete playlists, containing songs. playlists will show up on the user's profile page
- commenting and liking
- editing song information, and deleting songs
- with admin rights: ability to delete all songs, edit all profiles and song information
- possibly basic profile pictures? choose from a set of ASCII pictures

Songs:
- will have descriptions
- timestamps of the songs go unused currently: will be used to show when the song has been uploaded.
- implement likes and play count on songs

Front page:
- will have songs on it, possibly random songs
- will have a search bar, can also search for songs with a specific genre, songs that were uploaded this week/today...

Security:
- passwords saved in plain text currently. need to save them in hash
- browser cache may cause some issues security-wise later (I've been logged in as users that shouldn't exist anymore)

UI:
- will be fully in text, no images, or even buttons! this is by design, and will probably make things harder for me. (it was already hard making the seek bar in text) why? i just like the idea of it. will include ASCII art possibly to make it look better
- implement HTML layout extended to the templates

The user can:

- log in and out, and create a new account
- upload new music on the platform
- have a profile page that displays their music (with possibly a basic description set by the user)
- listen to other people's music and receive "medals" on their profile page (ex. "Biggest Rock Listener of the Day", "Most Listens on "Lady Gaga - Poker Face" This Month")
- increase the play count of other people's songs (not their own) by listening
- (maybe comments on songs and a basic follow/unfollow system could be implemented, or reposting other people's songs on your profile page: that will be determined later)
- search for songs containing a specific name or genre, songs that were uploaded today/this week/...

The songs:
- have an audio file connected to them (which format? yet to be determined, probably depends on the libraries used)
- have a title, and an artist/multiple artists
- have an upload date/time
- have a genre set by the uploader
- have a play count determined by how many times another user has pressed play on the song
- could possibly have cover art?
