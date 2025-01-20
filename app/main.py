from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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
@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def read_root():
    """
    Page racine avec un message de bienvenue et un lien vers la documentation.
    """
    return """
    <html>
        <head>
            <title>API CRUD</title>
        </head>
        <body>
            <h1>Bienvenue sur l'API CRUD avec authentification !</h1>
            <p><a href="/docs" target="_blank" style="text-decoration: none; color: blue;">Click ici !</a></p>
        </body>
    </html>
    """

# Inclusion des routes
app.include_router(auth_router, tags=["Authentification"])  # Route pour l'authentification
app.include_router(products.router, prefix="/products", tags=["Produits"])
