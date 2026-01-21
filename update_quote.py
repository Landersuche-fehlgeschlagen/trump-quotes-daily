import requests
import os
from datetime import datetime

# Configuration
API_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def get_recent_quote():
    # Consigne mise à jour : Focus auteur, Truth Social/X et Récence
    prompt = """
    TÂCHE : Trouve une citation RÉCENTE (idéalement des dernières 48h) et controversée (illégale, autoritaire, menaçante, fausse).
    CIBLE : Donald Trump, JD Vance (VP), Elon Musk, Pete Hegseth, ou membres clés du cabinet.
    SOURCES : Truth Social, X (Twitter), Discours officiels, Interviews.
    
    FORMAT DE RÉPONSE STRICT (Respecte exactement ce format) :
    Auteur : [Nom de la personne]
    Citation : "[Le texte exact de la citation]"
    Contexte : [Bref contexte : Truth Social, X, ou Discours à...]
    Source : [URL de la source]
    Date : [Date de la citation]
    """
    
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 500, "return_full_text": False, "temperature": 0.7}
    }
    
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()[0]['generated_text'].strip()
    except Exception as e:
        print(f"Erreur API : {e}")
        # Citation de secours si l'IA échoue
        return """
        Auteur : Donald Trump
        Citation : "Nous avons besoin de frontières fortes, pas de juges faibles."
        Contexte : Truth Social
        Source : https://truthsocial.com
        Date : Aujourd'hui
        """

def update_html():
    raw_text = get_recent_quote()
    
    # Parsing basique pour séparer les éléments (si le format est respecté)
    # On initialise des valeurs par défaut
    auteur = "Administration Trump"
    citation = raw_text
    contexte = "Déclaration récente"
    source = "#"
    
    lines = raw_text.split('\n')
    for line in lines:
        if line.startswith("Auteur :"):
            auteur = line.replace("Auteur :", "").strip()
        elif line.startswith("Citation :"):
            citation = line.replace("Citation :", "").strip().strip('"')
        elif line.startswith("Contexte :"):
            contexte = line.replace("Contexte :", "").strip()
        elif line.startswith("Source :"):
            source = line.replace("Source :", "").strip()

    today = datetime.now().strftime("%d/%m/%Y")
    
    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dérive : {today}</title>
    <link rel="stylesheet" href="style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,700&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Logo en haut à droite -->
    <img src="assets/logo.png" alt="Logo" class="logo-top-right" onerror="this.style.display='none'">

    <div class="container">
        <header>
            <p class="date">{today}</p>
        </header>

        <main>
            <!-- L'auteur en majuscules -->
            <div class="author">{auteur.upper()}</div>
            
            <!-- Le contexte (Truth Social, X...) -->
            <div class="context">{contexte}</div>

            <!-- La citation en rouge -->
            <blockquote class="quote">
                “{citation}”
            </blockquote>

            <!-- La source -->
            <div class="source">
                <a href="{source}" target="_blank">Voir la source originale →</a>
            </div>
        </main>
    </div>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ index.html mis à jour avec Auteur et Contexte.")

if __name__ == "__main__":
    update_html()
