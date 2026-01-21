import os
import re
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Configuration
API_KEY = os.environ.get("MISTRAL_API_KEY")
client = MistralClient(api_key=API_KEY)

def get_quote():
    # Prompt strict pour faciliter le découpage par le code
    prompt = """
    TÂCHE : Trouve une citation RÉCENTE et controversée de Donald Trump, JD Vance, ou Elon Musk.
    SUJET : Illégal, autoritaire, mensonge flagrant, ou référence fasciste.
    
    FORMAT DE RÉPONSE OBLIGATOIRE (Remplis juste les crochets) :
    AUTEUR: [Nom de la personne]
    CITATION: [La citation exacte entre guillemets]
    URL: [Lien http direct vers la source]
    SOURCE_NOM: [Nom du média, ex: The Guardian]
    DATE: [Date au format JJ/MM/AAAA]
    """
    
    try:
        chat_response = client.chat(
            model="mistral-large-latest",
            messages=[ChatMessage(role="user", content=prompt)]
        )
        content = chat_response.choices[0].message.content
        return content
    except Exception as e:
        print(f"Erreur API : {e}")
        return None

def parse_and_generate_html(raw_text):
    # Valeurs par défaut
    data = {
        "AUTEUR": "DONALD TRUMP",
        "CITATION": "Une erreur est survenue lors de la récupération.",
        "URL": "#",
        "SOURCE_NOM": "Source inconnue",
        "DATE": "Aujourd'hui"
    }
    
    # Découpage intelligent du texte de l'IA
    if raw_text:
        lines = raw_text.split('\n')
        for line in lines:
            if "AUTEUR:" in line:
                data["AUTEUR"] = line.split("AUTEUR:")[1].strip()
            elif "CITATION:" in line:
                data["CITATION"] = line.split("CITATION:")[1].strip().replace('"', '') # On enlève les guillemets pour les remettre en CSS ou HTML
            elif "URL:" in line:
                # Extraction basique d'URL
                url_match = re.search(r'(https?://[^\s]+)', line)
                if url_match:
                    data["URL"] = url_match.group(0)
            elif "SOURCE_NOM:" in line:
                data["SOURCE_NOM"] = line.split("SOURCE_NOM:")[1].strip()
            elif "DATE:" in line:
                data["DATE"] = line.split("DATE:")[1].strip()

    # Génération du HTML propre
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Citation du jour - Trump & Co</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="container">
            <div class="quote">« {data['CITATION']} »</div>
            <div class="author">{data['AUTEUR']}</div>
            
            <div class="meta">
                Source : <a href="{data['URL']}" target="_blank">{data['SOURCE_NOM']}</a> 
                — {data['DATE']}
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

if __name__ == "__main__":
    print("🔍 Recherche de la citation...")
    raw_text = get_quote()
    
    if raw_text:
        print("📝 Génération du site...")
        html = parse_and_generate_html(raw_text)
        
        with open("index.html", "w") as f:
            f.write(html)
        print("✅ index.html mis à jour avec succès.")
    else:
        print("❌ Échec de la récupération.")
