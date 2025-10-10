import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Vérifier si une URL a été donnée en argument
if len(sys.argv) < 2:
    print("❌ Utilisation : python test.py <URL>")
    sys.exit(1)

# Récupérer l’URL depuis les arguments
url = sys.argv[1]

# Créer un dossier pour stocker les images
os.makedirs("data", exist_ok=True)

# Télécharger la page
response = requests.get(url)
if response.status_code != 200:
    print(f"❌ Erreur lors du téléchargement de la page : {response.status_code}")
    sys.exit(1)

# Analyser la page HTML
soup = BeautifulSoup(response.text, "html.parser")

# Trouver toutes les balises <img>
images = soup.find_all("img")

print(f"🔍 {len(images)} images trouvées sur la page.")

# Extensions autorisées
extensions_valides = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

for img in images:
    img_url = img.get("src")
    if not img_url:
        continue

    # Construire l'URL complète
    img_url = urljoin(url, img_url)

    # Extraire le nom du fichier sans les paramètres
    parsed_url = urlparse(img_url)
    img_name = os.path.basename(parsed_url.path)

    # Vérifier si le format est valide
    if not img_name.lower().endswith(extensions_valides):
        print(f"🚫 Ignoré (format non valide) : {img_name}")
        continue

    # Chemin complet du fichier
    img_path = os.path.join("data", img_name)

    try:
        img_data = requests.get(img_url).content
        with open(img_path, "wb") as f:
            f.write(img_data)
        print(f"✅ Téléchargé : {img_path}")
    except Exception as e:
        print(f"⚠️ Erreur pour {img_url} : {e}")
