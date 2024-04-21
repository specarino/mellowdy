<p align="center">
  <img width="128" height="128" src="https://github.com/specarino/mellowdy/blob/main/assets/mellowdy-256px.png?raw=True">
</p>

# mellowdy

A basic Twitch chat bot hosted locally, designed to show the currently playing song, enable viewers to request tracks and view the current queue. Mods also have access to playback controls like pause, play, skip and volume.

# Installing from source
```sh
pip install -r requirements.txt
```
Create a file named `.env`. Populate the variables with info from [Spotify](https://developer.spotify.com/dashboard) and [Twitch](https://dev.twitch.tv/console)
```sh
SPOTIPY_CLIENT_ID=""
SPOTIPY_CLIENT_SECRET=""
SPOTIPY_REDIRECT_URI=""

TWITCH_APP_ID=""
TWITCH_APP_SECRET=""
```
(Optional) Create a file called `channels.txt` in case the bot is authorized using a different Twitch account than the one used for streaming. *By default, the code bot joins the channel of the user authenticated with Twitch.* Each line in the file represents a different channel's name.
```
channel_1
channel_2
etc.
```
Either run `main.py` to use the bot or pack it using,
```sh
python hooks/hook-generator.py
pyinstaller --onefile --runtime-hook hooks/hook-env-loader.py --name mellowdy --icon assets/mellowdy.ico main.py
```
*`hook-generator.py` loads environmental variables from `.env` and creates a file called `hook-env-loader.py` which hardcodes in the variables. This file is then packed in with the executeable. Is it safe to do this? Probably not.*

<a href="https://www.flaticon.com/free-icons/marshmallow" title="marshmallow icons">Marshmallow icons created by Freepik - Flaticon</a>
