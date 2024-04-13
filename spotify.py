import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID=os.getenv("SP_CLIENT_ID")
CLIENT_SECRET=os.getenv("SP_CLIENT_SECRET")
REDIRECT_URI=os.getenv("SP_REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-currently-playing user-modify-playback-state")
)

def get_currently_playing():
    song = sp.currently_playing()

    if song:
        title = song["item"]["name"]
        artists_json = song["item"]["artists"]
        artists = list()
        for artist in artists_json:
            artists.append(artist["name"])
        url = song["item"]["external_urls"]["spotify"]

        return f"{title} - {", ".join(artists)} | {url}"
    else:
        return "Nothing is playing."

def add_track_to_queue(query):
    results = sp.search(query, limit=1, type="track")
    if results["tracks"]["items"]:
        title = results["tracks"]["items"][0]["name"]

        artists_json = results["tracks"]["items"][0]["artists"]
        artists = list()
        for artist in artists_json:
            artists.append(artist["name"])

        uri = results["tracks"]["items"][0]["uri"]

        try:
            sp.add_to_queue(uri)
        except SpotifyException:
            return f"Spotify is not running."
        else:
            return f"Added {title} by {", ".join(artists)} to the queue!"
    else:
        return f"No results found for {query}"

if __name__ == "__main__":
    print(add_track_to_queue("metro future kendrick"))