from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.routers import products
from app.auth.auth import login

app = FastAPI(
    title="AdventureWorks Product API",
    description="API CRUD pour gérer les produits d'AdventureWorks",
    version="1.0.0"
)

# Inclusion du router pour les produits
app.include_router(products.router)

# Endpoint pour l'authentification
@app.post("/login", tags=["authentication"])
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login(form_data)
