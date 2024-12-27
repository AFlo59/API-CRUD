from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routers import products
from app.auth import auth

app = FastAPI(
    title="API CRUD AdventureWorks",
    description="API pour gérer les produits avec authentification OAuth2",
    version="1.0.0"
)

app.include_router(products.router)
app.include_router(auth.router)

@app.get("/", response_class=HTMLResponse)
def root():
    """
    Page d'accueil avec lien vers la documentation.
    """
    return """
    <html>
        <body>
            <h1>Bienvenue sur l'API AdventureWorks</h1>
            <p><a href="/docs">Documentation</a></p>
        </body>
    </html>
    """
