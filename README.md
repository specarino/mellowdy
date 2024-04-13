# Mellowdy

A basic Twitch chat bot hosted locally, designed to show the currently playing song and enable viewers to request tracks.

# Installing from source
```sh
pip install -r requirements.txt
```
Create a file named `.env`. Populate the variables with info from [Spotify](https://developer.spotify.com/dashboard) and [Twitch](https://dev.twitch.tv/console)
```sh
SP_CLIENT_ID=""
SP_CLIENT_SECRET=""
SP_REDIRECT_URI=""

TW_APP_ID=""
TW_APP_SECRET=""
```
(Optional) Create a file called `channels.txt` in case the bot is authorized using a different Twitch account than the one used for streaming. *By default, the code bot joins the channel of the user authenticated with Twitch.* Each line in the file represents a different channel's name.
```
channel_1
channel_2
etc.
```
Either run `main.py` to use the bot or pack it using,
```sh
pyinstaller --onefile --name mellowdy main.py
```