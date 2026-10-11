import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

# -------------------------------
DEEZER_COEURS_URL = "https://www.deezer.com/fr/profile/me/tracks"
SCROLL_PAUSE = 1.0
MAX_SCROLL = 50
# -------------------------------

options = webdriver.FirefoxOptions()
options.add_argument("--start-maximized")
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
driver.get(DEEZER_COEURS_URL)

input("Connecte-toi et appuie sur Entrée quand la page Coups de cœur est affichée...")

tracks = []
seen_tracks = set()

last_height = driver.execute_script("return document.body.scrollHeight")

for scroll_num in range(MAX_SCROLL):
    # scroll
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE)

    # récupérer tous les tracks visibles
    track_containers = driver.find_elements(By.CSS_SELECTOR, "div.JIYRe")

    for container in track_containers:
        try:
            # titre
            title_el = container.find_element(By.CSS_SELECTOR, "span[data-testid='title']")
            title = title_el.text.strip()

            # tous les artistes
            artist_els = container.find_elements(By.CSS_SELECTOR, "a[data-testid='artist']")
            artists = ", ".join([a.text.strip() for a in artist_els])

            key = (title, artists)
            if key not in seen_tracks:
                tracks.append({"title": title, "artist": artists})
                seen_tracks.add(key)
        except:
            continue

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    print(f"Scroll {scroll_num+1}/{MAX_SCROLL} effectué, {len(tracks)} titres récupérés...")

driver.quit()

# -------------------------------
df = pd.DataFrame(tracks)
df.to_csv("deezer_coups_de_coeur.csv", index=False, encoding="utf-8-sig")

with open("deezer_coups_de_coeur.txt", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        f.write(f"{row['artist']} - {row['title']}\n")

print(f"\n✅ Export terminé : {len(df)} titres récupérés")
