import requests
import pandas as pd

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

        url = data.get("next")  # pagination Deezer

    df = pd.DataFrame(tracks)

    # Export CSV
    df.to_csv("deezer_playlist.csv", index=False, encoding="utf-8-sig")

    # Export TXT (optionnel)
    with open("deezer_playlist.txt", "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            f.write(f"{row['artist']} - {row['title']}\n")

    print(f"Export terminé : {len(df)} titres")
