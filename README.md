# API CRUD AdventureWorks

Cette API permet d'interagir avec la base de données **AdventureWorks** hébergée sur **Azure SQL**.

## Fonctionnalités
- **CRUD** sur les produits (table `Production.Product`).
- **Authentification** OAuth2 avec JSON Web Tokens (JWT).

## Dépendances
Voir [requirements.txt](requirements.txt).

## Installation
1. Cloner ce dépôt
2. Créer et activer un virtualenv (facultatif)
3. Installer les dépendances:
   ```bash
   pip install -r requirements.txt


```fastapi-adventureworks/
├── .env                       # Nouveau fichier contenant les variables secrètes
├── .gitignore                 # Ajouter .env ici pour l’exclure du dépôt
├── app/
│   ├── main.py            # Point d'entrée de l’application
│   ├── database.py        # Configuration de la connexion à la BDD
│   ├── models.py          # Modèles SQLModel
│   ├── schemas.py         # Schémas Pydantic/SQLModel (facultatif si on segmente)
│   ├── auth/
│   │   ├── auth.py        # Logique d'authentification
│   │   └── security.py    # Gestion du token JWT, hashing mot de passe, etc.
│   ├── routers/
│   │   └── products.py    # Routes CRUD pour les produits
│   └── config.py          # Paramètres de configuration (DB_URI, secret_key, etc.)
├── requirements.txt           # Mis à jour pour inclure toutes les dépendances
└── README.md```
