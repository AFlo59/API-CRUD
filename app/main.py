from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
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

# Configurer les templates
templates_dir = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=templates_dir)

# Servir les fichiers statiques (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def read_root(request: Request):
    """
    Page racine avec un message de bienvenue et un lien vers la documentation.
    """
    return templates.TemplateResponse("index.html", {"request": request})


# Inclusion des routes
app.include_router(auth_router, tags=["Authentification"])  # Route pour l'authentification
app.include_router(products.router, prefix="/products", tags=["Produits"])  # Route pour les produits
