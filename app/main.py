from fastapi import FastAPI
from app.routers import products

# Création de l'application
app = FastAPI(
    title="API CRUD avec Authentification",
    description="""API pour gérer les produits avec un système d'authentification sécurisé basé sur OAuth2 et JWT.
    ### Fonctionnalités :
    1. **Authentification** : Génération de tokens pour sécuriser les routes.
    2. **Gestion des produits** :
        - Lister les produits.
        - Consulter un produit spécifique.
        - Ajouter un produit.
        - Modifier un produit existant.
        - Supprimer un produit.
    """,
    version="1.0.0",
)

# Inclusion des routes pour les produits
app.include_router(products.router, prefix="/products", tags=["Produits"])

