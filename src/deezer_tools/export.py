import json
import pandas as pd

from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

def create_scan_directory():

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    existing_numbers = []

    for folder in DATA_DIR.iterdir():
        if folder.is_dir() and folder.name.startswith("scan"):
            suffix = folder.name[4:]

            if suffix.isdigit():
                existing_numbers.append(int(suffix))

    next_number = max(existing_numbers, default=0) + 1

    scan_dir = DATA_DIR / f"scan{next_number}"
    scan_dir.mkdir()

    return scan_dir

def export_tracks(tracks, scan_dir): # tracks must contain 'artist' and 'title' keys

    df = pd.DataFrame(
        tracks,
        columns=["title", "artist"]
    )

    csv_path = scan_dir / "deezer_songs.csv"

    df.to_csv(
        csv_path,
        index=False,
        encoding="utf-8-sig",
        sep=";"
    )

    txt_path = scan_dir / "deezer_songs.txt"

    with open(txt_path, "w", encoding="utf-8") as f:
        for track in tracks:
            f.write(
                f"{track['artist']} - {track['title']}\n"
            )

    json_path = scan_dir / "deezer_songs.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            tracks,
            f,
            ensure_ascii=False,
            indent=2
        )

    # Informations générales sur le scan
    scan_info = {
        "scan_date": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "track_count": len(tracks),
        "files": [
            csv_path.name,
            txt_path.name,
            json_path.name
        ]
    }

    info_path = scan_dir / "scan_info.json"

    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(
            scan_info,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("\n--- EXPORT TERMINÉ ---")
    print(f"\nDossier : {scan_dir}")

    return scan_dir
