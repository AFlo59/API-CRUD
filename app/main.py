from fastapi import FastAPI
from app.routers import products
from app.routers.auth_routes import router as auth_router

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

# Route racine
@app.get("/", tags=["Root"])
async def read_root():
    """
    Page racine avec un message de bienvenue et un lien vers la documentation.
    """
    return {
        "message": "Bienvenue sur l'API CRUD avec authentification !",
        "documentation_url": "http://127.0.0.1:8000/docs"
    }

# Inclusion des routes
app.include_router(auth_router)  # Route pour l'authentification
app.include_router(products.router, prefix="/products", tags=["Produits"])
