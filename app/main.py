from fastapi import FastAPI
from app.routers import products
from app.auth.auth import login

app = FastAPI(
    title="API CRUD AdventureWorks",
    description="API pour gérer les produits avec authentification OAuth2",
    version="1.0.0"
)

# Inclusion des routes
app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API AdventureWorks"}
