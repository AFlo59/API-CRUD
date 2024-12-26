# **API CRUD AdventureWorks**

Cette API permet d'interagir avec la base de données **AdventureWorks** hébergée sur **Azure SQL**. Elle inclut une gestion des produits (CRUD) et un système d'authentification sécurisé basé sur OAuth2 avec JWT.

---

## **Fonctionnalités principales**

- **Authentification sécurisée :**
  - Génération de tokens JWT via `/login`.
  - Protection des routes via OAuth2.

- **CRUD des produits :**
  - **Lister les produits** : `GET /products/`
  - **Récupérer un produit spécifique** : `GET /products/{product_id}`
  - **Créer un nouveau produit** : `POST /products/`
  - **Mettre à jour un produit existant** : `PUT /products/{product_id}`
  - **Supprimer un produit** : `DELETE /products/{product_id}`

---

## **Installation**

### **Prérequis**
- Python 3.9 ou supérieur.
- Pilote ODBC : `ODBC Driver 18 for SQL Server`.
- Une base de données Azure SQL configurée.

### **Étapes**

1. **Cloner ce dépôt** :

```bash
git clone https://github.com/AFlo59/API-CRUD.git
cd ./API-CRUD
```

### Créer un environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
.\venv\Scripts\activate   # Sur Windows
```
## Dépendances
Voir [requirements.txt](requirements.txt).

### Installer les dépendances :

```bash
pip install -r requirements.txt
```
### Configurer les variables d'environnement :
   Créez un fichier .env à la racine avec les informations suivantes :

```
env

DB_SERVER="adventureworks-server-hdf.database.windows.net"
DB_NAME="adventureworks"
DB_USER="jvcb"
DB_PASSWORD="cbjv592023!"
DB_PORT=1433
SECRET_KEY="your_secret_key"  # Peut être générée dynamiquement
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
ODBC_DRIVER="ODBC Driver 18 for SQL Server"
```
### Lancer l'application :

```bash
uvicorn app.main:app --reload
```

## Structure du projet

```
api-crud/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entrée principale de l'application
│   ├── config.py            # Configuration de l'application
│   ├── database.py          # Connexion à la base de données
│   ├── models.py            # Définition des modèles SQL
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── auth.py          # Gestion de l'authentification
│   │   ├── security.py      # Gestion des tokens et mots de passe
│   ├── routers/
│       ├── __init__.py
│       ├── products.py      # Routes CRUD pour les produits
├── .env                     # Fichier d'environnement
├── requirements.txt         # Dépendances du projet
├── README.md                # Documentation du projet
```
