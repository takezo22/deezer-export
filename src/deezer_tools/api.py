import requests
from deezer_tools.export import *


def run_api_playlist(playlist_id):
    BASE_URL = f"https://api.deezer.com/playlist/{playlist_id}/tracks"

    tracks = []
    url = BASE_URL

    while url:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        for track in data["data"]:
            tracks.append({
                "title": track["title"],
                "artist": ", ".join(artist["name"] for artist in track.get("contributors", []))
                          or track["artist"]["name"],
                "album": track["album"]["title"],
                "duration_sec": track["duration"],
                "rank": track["rank"],
                "explicit": track["explicit_lyrics"],
            })

        url = data.get("next")
    scan_dir = create_scan_directory()
    export_tracks(tracks, scan_dir)

    return tracks


