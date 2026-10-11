import time
from deezer_tools.export import *
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait

def run_scraper():
    DEEZER_COEURS_URL = "https://www.deezer.com/fr/library/loved"

    SCROLL_PAUSE = 1.5
    MAX_SCROLL = 1000
    MAX_IDLE_SCROLLS = 8

    options = webdriver.FirefoxOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()),
        options=options
    )

    tracks = []
    seen_tracks = set()
    idle_scrolls = 0

    try:
        driver.get(DEEZER_COEURS_URL)

        input("Connecte-toi et affiche tes Coups de cœur, puis appuie sur Entrée.")
        print("Début du scan...")
        time_start = time.time()

        # Attendre que le document soit prêt
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(3)

        for scroll_num in range(MAX_SCROLL):

            # 1. Lire les titres actuellement présents dans le DOM
            track_containers = driver.find_elements(
                By.CSS_SELECTOR, "div.JIYRe"
            )

            before_count = len(seen_tracks)

            for container in track_containers:
                try:
                    title_el = container.find_element(
                        By.CSS_SELECTOR,
                        "[data-testid='title']"
                    )
                    title = title_el.text.strip()

                    artist_els = container.find_elements(
                        By.CSS_SELECTOR,
                        "a[data-testid='artist']"
                    )
                    artists = ", ".join(
                        a.text.strip()
                        for a in artist_els
                        if a.text.strip()
                    )

                    if not title:
                        continue

                    key = (title, artists)

                    if key not in seen_tracks:
                        seen_tracks.add(key)
                        tracks.append({
                            "title": title,
                            "artist": artists
                        })

                except Exception:
                    continue

            new_tracks = len(seen_tracks) - before_count

            print(
                f"Passage {scroll_num + 1} | "
                f"{len(tracks)} titres récupérés | "
                f"(+{new_tracks})"
            )

            # 2. Détecter si le scraping progresse
            if new_tracks > 0:
                idle_scrolls = 0
            else:
                idle_scrolls += 1

            if idle_scrolls >= MAX_IDLE_SCROLLS:
                print("Plus de titres détectés, fin du scan.")
                break

            # 3. Défiler progressivement
            driver.execute_script("window.scrollBy(0, 400);")
            time.sleep(SCROLL_PAUSE)
    finally:
        driver.quit()
    
    duration = time.time() - time_start
    print(f"\nScan terminé : {len(tracks)} titres récupérés.")
    print(f"Durée : {duration:.2f} secondes.")

    scan_dir = create_scan_directory()
    export_tracks(tracks, scan_dir)

    return tracks


if __name__ == "__main__":
    run_scraper()