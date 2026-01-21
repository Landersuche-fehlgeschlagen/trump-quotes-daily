import os
import json
from datetime import datetime
from mistralai import Mistral
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    raise ValueError("La clé API Mistral n'est pas définie.")

def get_trump_quote():
    client = Mistral(api_key=API_KEY)

    # On demande un JSON strict pour avoir le lien et la date séparés
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": """
                Trouve une citation controversée ou marquante de Donald Trump ou de son entourage (JD Vance, Elon Musk...).
                Privilégie une actualité récente (dernières 48h) si possible, sinon une phrase culte.
                
                FORMAT DE RÉPONSE ATTENDU (JSON BRUT UNIQUEMENT) :
                {
                    "citation": "Le texte exact de la citation en français",
                    "auteur": "Le nom de l'auteur (ex: Donald Trump)",
                    "source_nom": "Nom du média (ex: Fox News, X/Twitter)",
                    "url": "Lien URL vers la source",
                    "date": "Date de la citation (ex: 20 Janvier 2025)"
                }
                """
            }
        ]
    )
    
    content = response.choices[0].message.content
    
    # Nettoyage des balises Markdown si l'IA en met
    if "```json" in content:
        content = content.replace("```json", "").replace("```", "")
    
    return json.loads(content.strip())

def update_html(data):
    # Récupération des données du JSON
    citation = data.get("citation", "Citation introuvable")
    auteur = data.get("auteur", "Donald Trump")
    source_nom = data.get("source_nom", "Source")
    url = data.get("url", "#")
    date = data.get("date", "")

    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dérive : {auteur}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <img src="assets/logo.png" alt="Logo Dérive" class="logo-top-right">
        <!-- La citation en rouge -->
        <div class="quote">
            « {citation} »
        </div>
        
        <!-- L'auteur en dessous -->
        <div class="author">
            — {auteur}
        </div>
        
        <!-- Source cliquable et date -->
        <div class="meta">
            Vu sur <a href="{url}" target="_blank">{source_nom}</a> • {date}
        </div>
    </div>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ index.html mis à jour avec le nouveau design.")

def main():
    try:
        data = get_trump_quote()
        update_html(data)
    except Exception as e:
        print(f"❌ Erreur : {e}")
        raise e

if __name__ == "__main__":
    main()
