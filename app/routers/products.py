from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models import Product, ProductCreate, ProductRead
from app.auth.security import oauth2_scheme, verify_token
from typing import List


router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductRead])
def read_products(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    """
    Récupère tous les produits. Nécessite un token valide.
    """
    payload = verify_token(token)
    return session.exec(select(Product)).all()
