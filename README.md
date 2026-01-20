# Trump Quotes Daily

Un site minimaliste affichant **une citation controversée de Donald Trump ou de son administration** chaque jour, sourcée et archivée.

## 📌 Fonctionnalités
- **Citation quotidienne** automatiquement mise à jour via GitHub Actions.
- **Sources vérifiées** (médias fiables uniquement).
- **Archive complète** dans `citations.json`.
- **Design épuré** : Times New Roman, citation en rouge sur fond blanc.

## 🛠 Installation
1. Cloner le repo :
   ```bash
   git clone https://github.com/votre-utilisateur/trump-quotes-daily.git
   cd trump-quotes-daily

2. Créer un environnement virtuel :

    python3 -m venv venv
    source venv/bin/activate  # macOS/Linux
    venv\Scripts\activate    # Windows

3. Installer les dépendances :

    pip install -r requirements.txt

4. Ajouter votre clé API Mistral dans .env :

    echo "MISTRAL_API_KEY=votre_clé_api" > .env

5. Tester localement :

    python update_quote.py

