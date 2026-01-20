import os
import json
from datetime import datetime
from mistralai import Mistral
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé API
API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    raise ValueError("La clé API Mistral n'est pas définie dans .env")

def get_trump_quote():
    """Récupère une citation controversée de Trump via l'API Mistral (v1.x)."""
    # Initialisation du client (Nouvelle syntaxe)
    client = Mistral(api_key=API_KEY)

    # Appel au modèle (Nouvelle syntaxe : .complete)
    chat_response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": """
                **INSTRUCTIONS STRICTES** :
                1. Trouve UNE SEULE citation **exacte** de Donald Trump ou de son administration (2015-2025), **controversée** ou marquante.
                   - Sujets : Immigration, Justice, Élections, Opposants politiques, International.
                2. Format de sortie OBLIGATOIRE (JSON brut uniquement) :
                {
                    "text": "La citation exacte ici.",
                    "source": "Nom du média (ex: CNN, Fox News)",
                    "url": "Lien vers l'article source",
                    "date": "JJ/MM/AAAA"
                }
                3. Règles :
                - Réponds UNIQUEMENT avec le JSON. Rien d'autre avant ou après.
                - La citation doit être en français (traduite si nécessaire).
                """
            }
        ],
        temperature=0.3
    )

    # Extraction du contenu
    content = chat_response.choices[0].message.content
    
    # Nettoyage si le modèle ajoute des balises ```json
    if "```" in content:
        content = content.replace("```json", "").replace("```", "").strip()
        
    return content

def update_website(json_data):
    """Met à jour index.html et l'historique."""
    try:
        data = json.loads(json_data)
        quote = data.get("text")
        source = data.get("source")
        url = data.get("url")
        date = data.get("date")
    except json.JSONDecodeError:
        print("Erreur : La réponse de l'IA n'est pas un JSON valide.")
        print("Réponse reçue :", json_data)
        return

    # 1. Mettre à jour index.html
    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>La Citation du Jour - Trump</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>🤡 La Citation du Jour</h1>
        <div class="quote-box">
            <p class="quote">"{quote}"</p>
            <p class="meta">
                Source : <a href="{url}" target="_blank">{source}</a><br>
                Date : {date}
            </p>
        </div>
        <footer>
            <p>Mise à jour automatique par IA | <a href="https://github.com/votre-utilisateur/trump-quotes-daily">Code Source</a></p>
        </footer>
    </div>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ index.html mis à jour avec succès.")

    # 2. Sauvegarder dans l'historique (citations.json)
    history_file = "citations.json"
    history = []
    
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

    # Ajouter la nouvelle citation
    history.insert(0, data) # Ajouter au début

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)
    
    print("✅ Historique sauvegardé.")

def main():
    print("🔍 Recherche d'une citation controversée de Trump...")
    try:
        quote_json = get_trump_quote()
        if quote_json:
            update_website(quote_json)
        else:
            print("❌ Aucune donnée reçue.")
    except Exception as e:
        print(f"❌ Une erreur critique est survenue : {e}")
        # On lève l'erreur pour que GitHub Actions marque le job comme échoué
        raise e 

if __name__ == "__main__":
    main()
