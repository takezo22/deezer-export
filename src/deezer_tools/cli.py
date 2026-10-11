import argparse
from deezer_tools.scraper import run_scraper
from deezer_tools.api import run_api_playlist

def main():
    parser = argparse.ArgumentParser(description="Outils de récupération de musiques Deezer.")
    
    parser.add_argument(
        "--loved", 
        action="store_true", 
        help="Récupère les coups de cœur via Selenium"
    )
    parser.add_argument(
        "--playlist", 
        type=str, 
        help="Récupère les musiques d'une playlist via l'API Deezer (fournir l'ID)"
    )
    
    args = parser.parse_args()

    if args.loved:
        run_scraper()
    elif args.playlist:
        run_api_playlist(args.playlist)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
