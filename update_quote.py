import os
import json
from datetime import datetime
from mistralai.client import MistralClient
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé API
API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    raise ValueError("La clé API Mistral n'est pas définie dans .env")

def get_trump_quote():
    """Récupère une citation controversée de Trump via l'API Mistral."""
    client = MistralClient(api_key=API_KEY)

    response = client.chat(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": """
                **INSTRUCTIONS STRICTES** :
                1. Trouve UNE SEULE citation **exacte** de Donald Trump ou de son administration (2015-2024), **controversée** :
                   - Raciste, sexiste, xénophobe
                   - Antidémocratique ou autoritaire
                   - Liée à l'extrême droite, au fascisme, ou au nazisme
                   - Illégale ou inhumaine (ex: séparation des familles migrantes)
                2. Format de sortie OBLIGATOIRE (ne dévie pas) :
                ```
                "Citation exacte entre guillemets."
                Source : [URL_complète] (Date : JJ/MM/AAAA)
                ```
                3. Règles :
                - Utilise UNIQUEMENT des sources fiables : Washington Post, NY Times, The Guardian, BBC, PBS, NPR, AP News.
                - Si la citation n'est pas sourcée ou ne correspond pas aux critères, réponds : "Aucune citation valide trouvée."
                - Pas de commentaire, pas d'analyse, pas de modification.
                """
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

def update_website(quote_data):
    """Met à jour index.html avec la nouvelle citation."""
    if "Aucune citation valide" in quote_data:
        print("Aucune citation valide aujourd'hui.")
        return False

    try:
        quote_text = quote_data.split('\n')[0].strip('"')
        source_line = quote_data.split('\n')[1]
        source_url = source_line.split('[')[1].split(']')[0]
        source_date = source_line.split('(')[1].split(')')[0]

        # Lire le template HTML
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        # Remplacer les placeholders
        updated_html = html_content.replace(
            '<div id="quote" class="quote">\n            <!-- La citation sera insérée ici par le script Python -->\n            "Chargement de la citation..."\n        </div>',
            f'<div id="quote" class="quote">{quote_text}</div>'
        ).replace(
            '<div id="source" class="source">\n            <!-- La source sera insérée ici -->\n        </div>',
            f'<div id="source" class="source">Source : <a href="https://{source_url}">{source_url}</a> (Date : {source_date})</div>'
        )

        # Écrire le nouveau HTML
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(updated_html)

        print("Site mis à jour avec succès !")
        return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour du site : {e}")
        return False

def save_to_archive(quote_data):
    """Sauvegarde la citation dans citations.json."""
    try:
        quote_text = quote_data.split('\n')[0].strip('"')
        source_line = quote_data.split('\n')[1]
        source_url = source_line.split('[')[1].split(']')[0]
        source_date = source_line.split('(')[1].split(')')[0]

        # Charger l'archivage existant
        try:
            with open("citations.json", "r", encoding="utf-8") as f:
                archive = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            archive = []

        # Ajouter la nouvelle citation
        archive.append({
            "quote": quote_text,
            "source": f"https://{source_url}",
            "date": source_date,
            "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Sauvegarder
        with open("citations.json", "w", encoding="utf-8") as f:
            json.dump(archive, f, indent=2, ensure_ascii=False)

        print("Citation archivée avec succès !")
    except Exception as e:
        print(f"Erreur lors de l'archivage : {e}")

def main():
    print("🔍 Recherche d'une citation controversée de Trump...")
    quote_data = get_trump_quote()
    print(f"Citation trouvée :\n{quote_data}")

    if "Aucune citation valide" not in quote_data:
        if update_website(quote_data):
            save_to_archive(quote_data)
        else:
            print("Échec de la mise à jour du site.")
    else:
        print("Aucune citation valide aujourd'hui.")

if __name__ == "__main__":
    main()
