
# Instructions pour initialiser et lancer le projet

Ce projet est composé de deux parties principales : le backend, construit avec FastAPI, et le frontend, développé avec React.

## Configuration du Backend (FastAPI)

1. **Aller dans le répertoire du backend**:
   Ouvrez un terminal et naviguez vers le répertoire `back-end` en utilisant la commande :
   ```
   cd back-end
   ```

2. **Installation des dépendances**:
   Installez toutes les dépendances nécessaires en exécutant :
   ```
   pip install -r requirements.txt
   ```

3. **Création de la base de données SQLITE**:
   Si le fichier `blog.db` n'est pas présent dans le dossier `back-end`, exécutez le script `db.py` pour créer la base de données SQLite et la placer dans le dossier `back-end`.

4. **Lancement du serveur FastAPI**:
   Lancez le serveur FastAPI en utilisant uvicorn avec la commande suivante :
   ```
   uvicorn main:app --reload
   ```
   Ici, `main` est le nom du fichier Python qui crée l'instance de l'application FastAPI et `app` est l'instance de l'application FastAPI.

   Le serveur sera accessible à l'adresse `http://127.0.0.1:8000`.

## Configuration du Frontend (React)

Assurez-vous que le serveur FastAPI est en cours d'exécution avant de lancer le frontend.

1. **Aller dans le répertoire du frontend**:
   Ouvrez un nouveau terminal et naviguez vers le répertoire `api_app` en utilisant la commande :
   ```
   cd api_app
   ```

2. **Installation des dépendances React**:
   Installez toutes les dépendances nécessaires pour le projet React en exécutant :
   ```
   npm install
   ```
   ou si vous utilisez yarn :
   ```
   yarn install
   ```

3. **Lancement de l'application React**:
   Démarrez l'application React en utilisant la commande :
   ```
   npm start
   ```
   ou si vous utilisez yarn :
   ```
   yarn start
   ```

   L'application sera accessible à l'adresse `http://localhost:3000`.

---

Suivez ces étapes pour configurer et lancer votre projet FastAPI et React.
