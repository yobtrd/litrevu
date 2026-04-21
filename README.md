# Litrevu

Application web communautaire permettant aux utilisateurs de partager et demander des critiques littéraires.

## Fonctionnalités

- **Comptes utilisateurs** : Inscription/connexion sécurisée avec gestion de profil
- **Administration** : Interface dédiée avec droits étendus
- **Publications** :
  - Création de billets (livres/articles)
  - Rédaction de critiques avec notation par étoiles (1-5)
  - Édition/suppression des contenus (CRUD)
- **Réseau social** :
  - Abonnements asymétriques (follow/unfollow)
  - Recherche d'utilisateurs
  - Blocage de comptes
- **Flux personnalisé** : Affichage chronologique des publications des utilisateurs suivis
- **Accessibilité** : 
  - Design responsive adapté à tous les appareils
  - Normes d'accessibilité conformes au référentiel WCAG

### Stack technique

**Backend** :  
- Django (framework Python)

**Frontend** :  
- Tailwind CSS (utility-first CSS framework)  
- DaisyUI (composants Tailwind prêts à l'emploi)  
- Heroicons (bibliothèque d'icônes SVG)

**Packages Django** :  
- django-el-pagination ([lien PyPI](https://pypi.org/project/django-el-pagination/)) - pagination "infinite scroll"
- django-tailwind ([lien PyPi](https://pypi.org/project/django-tailwind/)) - Tailwind CSS intégration pour Django
- django-browser-reload ([lien PyPi](https://pypi.org/project/django-browser-reload/)) - Actualisation du navigateur à chaque modification du code

**Base de données** :  
- SQLite (développement)  

## Prérequis

- Python `3.8+` ;
- (Optionnel) Git pour cloner le dépôt ;
- (Optionnel) Node.JS pour utiliser django-tailwind en mode développement ;
- Compatible avec n'importe quel OS (Windows/Linux/macOS).

## Installation

- Cloner ou sauvegarder le dépôt à l'emplacement de votre choix ;
- Déplacer vous dans le dossier du dépôt ("litrevu"), qui deviendra votre répertoire de travail ;
- Créer un environnement virtuel pour installer les dépendances.  
Pour ce faire, dans le répertoire de travail :

```bash
python -m venv env
```

- Puis activer l'environnement virtuel avec :

```bash
source env/bin/activate # Ou source env/scripts/activate pour windows
```

- Enfin, installer les dépendances.  
Pour ce faire, dans le répertoire de travail:

```bash
pip install -r requirements.txt
```

## Usage

- Depuis le répertoire de travail, une fois votre environnement virtuel activé, déplacer vous dans le répertoire principal de l'application :

```bash
cd litrevu/
```

- Puis démarrer le serveur :

```bash
python manage.py runserver # ou py manage.py runserver sur windows
```

- Rendez-vous sur l'application avec le navigateur de votre choix via l'adresse :

http://127.0.0.1:8000/

- Créez vous un compte ou utiliser un compte fourni dans la BDD via les informations de connexion disponibles ci-dessous.

### Mode développement

Le CSS généré via django-tailwind est actuellement optimisé pour la production (notamment via PurgeCSS).  
Revenir en mode développement de django-tailwind et profiter de django-browser-reload nécessite Node.js (v14+ recommandée) et l'installation des dépendances.  
Pour ce faire, depuis le répertoire principal de l'application, déplacez vous dans le dossier static_src :

```bash
cd theme/static_src
```

- Installer les dépendances NPM avec :

```bash
npm install
```

Une fois l'environnement correctement installé, et une fois le serveur démarré dans un terminal :  
- Lancer un second terminal et saisissez la commande suivante :


```bash
python manage.py tailwind start
```

Et pour créer à nouveau une version compilée pour la production :

```bash
python manage.py tailwind build
```

Pour plus d'informations, se référer à la [documentation](https://django-tailwind.readthedocs.io/en/latest/index.html) de Django-Tailwind.

## Base de données de démonstration

Un fichier SQLite est inclus avec le repository et contient des données de test afin de faciliter l'aperçu des fonctionnalités.

Vous pouvez vous connecter aux différents utilisateurs factices via ces informations de connexion :

| Rôle          | Identifiant | Mot de passe    |
|---------------|-------------|-----------------|
| Administrateur| superuser   | superuser123    |
| Utilisateur 1 | user1       | utilisateur1    |
| Utilisateur 2 | user2       | utilisateur2    |
| Utilisateur 3 | user3       | utilisateur3    |
| Utilisateur 4 | user4       | utilisateur4    |
