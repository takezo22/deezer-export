import requests
from deezer_tools.export import *

import time
from collections import Counter


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



def stats(playlist_id):
    playlist_id = str(playlist_id).strip()

    session = requests.Session()
    session.headers.update({
        "User-Agent": "deezer-tools/1.0"
    })

    def get_json(url):
        """Effectue une requête et détecte les erreurs de l'API."""
        response = session.get(url, timeout=20)
        response.raise_for_status()

        try:
            payload = response.json()
        except ValueError as exc:
            raise RuntimeError(
                f"Deezer n'a pas renvoyé de JSON valide pour {url}. "
                f"Réponse : {response.text[:500]}"
            ) from exc

        if not isinstance(payload, dict):
            raise RuntimeError(
                f"Format de réponse inattendu pour {url}: {payload!r}"
            )

        if "error" in payload:
            raise RuntimeError(
                f"Erreur de l'API Deezer pour {url}: "
                f"{payload['error']!r}"
            )

        return payload

    try:
        # 1. Récupérer les titres de toutes les pages
        url = (
            f"https://api.deezer.com/playlist/"
            f"{playlist_id}/tracks"
        )

        tracks = []

        while url:
            payload = get_json(url)

            if not isinstance(payload.get("data"), list):
                raise RuntimeError(
                    f"Réponse sans liste 'data' pour {url}. "
                    f"Clés reçues : {list(payload.keys())}. "
                    f"Réponse : {payload!r}"
                )

            for track in payload["data"]:
                album = track.get("album") or {}
                artist = track.get("artist") or {}

                contributors = track.get("contributors") or []

                artist_names = ", ".join(
                    item["name"]
                    for item in contributors
                    if item.get("name")
                )

                tracks.append({
                    "title": track.get("title", ""),
                    "artist": (
                        artist_names or artist.get("name", "")
                    ),
                    "album": album.get("title", ""),
                    "album_id": album.get("id"),
                })

            url = payload.get("next")

        if not tracks:
            print("La playlist ne contient aucun titre.")
            return

        print(f"{len(tracks)} titres récupérés.")

        # 2. Récupérer les albums distincts une seule fois
        album_ids = {
            track["album_id"]
            for track in tracks
            if track["album_id"] is not None
        }

        album_genres = {}

        for album_id in sorted(album_ids):
            url_album = f"https://api.deezer.com/album/{album_id}"
            album_data = get_json(url_album)

            genre_block = album_data.get("genres") or {}
            genre_items = genre_block.get("data") or []

            genres = [
                item["name"]
                for item in genre_items
                if item.get("name")
            ]

            album_genres[album_id] = list(dict.fromkeys(genres))

            time.sleep(0.1)

        # 3. Compter les genres associés aux titres
        genre_counts = Counter()

        for track in tracks:
            genres = album_genres.get(track["album_id"], [])

            if not genres:
                genres = ["Genre inconnu"]

            for genre in genres:
                genre_counts[genre] += 1

        # 4. Afficher les statistiques
        total_tracks = len(tracks)
        total_associations = sum(genre_counts.values())

        print("\n--- STATISTIQUES DE LA PLAYLIST ---")
        print(f"Nombre de titres : {total_tracks}")
        print(f"Albums distincts : {len(album_ids)}")
        print(f"Genres recensés : {len(genre_counts)}")

        print("\nRépartition par genre :")

        for genre, count in genre_counts.most_common():
            pct_tracks = 100 * count / total_tracks
            pct_associations = (
                100 * count / total_associations
            )

            print(
                f"{genre}: {count} associations de titres "
                f"({pct_tracks:.1f}% des titres ; "
                f"{pct_associations:.1f}% des associations)"
            )

    finally:
        session.close()