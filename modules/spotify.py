import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID=os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET=os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI=os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE="user-read-currently-playing user-read-playback-state user-modify-playback-state"


def auth():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE)
)


def get_username() -> str:
    sp = auth()
    user = sp.current_user()
    return user["display_name"]


def get_currently_playing() -> str:
    sp = auth()
    song = sp.currently_playing()

    if song:
        title = song["item"]["name"]
        artists_json = song["item"]["artists"]
        artists = list()
        for artist in artists_json:
            artists.append(artist["name"])
        url = song["item"]["external_urls"]["spotify"]

        return f"{title} - {", ".join(artists)} // {url}"
    else:
        return "Nothing is playing."


def add_track_to_queue(query: str) -> str:
    sp = auth()
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
    

def get_next_in_queue(amount: int = 1, bound: int = 10) -> str:
    sp = auth()

    if amount > bound: amount = bound
    if amount < 1: amount = 1

    results = sp.queue()
    queue = results["queue"]

    if queue:
        titles = list()

        for index in range(amount):
            title = queue[index]["name"]
            titles.append(title)
            if amount == 1:
                artists_json = queue[index]["artists"]
                artists = list()
                for artist in artists_json:
                    artists.append(artist["name"])
                track = f"{title} by {", ".join(artists)}"

        if amount == 1:
            return track
        else:
            return " // ".join(titles)
    else:
        return "Nothing in queue!"
    

def goto_next_track():
    sp = auth()

    song = get_currently_playing()
    stripped = song.split(" // ", 1)[0]

    try:
        sp.next_track()
    except Exception:
        return f"Failed to skip track!"
    else:
        return f"Skipped {stripped}"


def goto_prev_track():
    sp = auth()

    song = get_currently_playing()
    stripped = song.split(" // ", 1)[0]
    
    try:
        sp.previous_track()
    except Exception:
        return f"Failed to rewind track!"
    else:
        return f"Rewinding to {stripped}"
    

def pause_current_track():
    sp = auth()

    try:
        sp.pause_playback()
    except Exception as error:
        if error.args[0] == 403:
            return "Track already paused!"
        else:
            return "Failed to resume track!"
    else:
        song = get_currently_playing()
        stripped = song.split(" // ", 1)[0]
        return f"Paused {stripped}"
    

def resume_current_track():
    sp = auth()

    try:
        sp.start_playback()
    except Exception as error:
        if error.args[0] == 403:
            return "Track already playing!"
        else:
            return "Failed to resume track!"
    else:
        song = get_currently_playing()
        stripped = song.split(" // ", 1)[0]
        return f"Resumed {stripped}"
    
def set_volume(volume: int):
    sp = auth()

    if volume > 100 : volume = 100
    if volume < 0: volume = 0

    try:
        sp.volume(volume)
    except Exception:
            return f"Failed to change volume!"
    else:
        return f"Volume: {volume}%"


def main():
    print("Waiting on Spotify authentication...")
    sp = auth()
    if sp.current_user():
        print("Spotify authenticated!")


main()