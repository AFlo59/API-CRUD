from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models import Product, ProductCreate, ProductRead
from app.auth.auth import oauth2_scheme, verify_token

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductRead])
def read_products(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    return session.exec(select(Product)).all()

@router.post("/", response_model=ProductRead)
def create_product(product_data: ProductCreate, session: Session = Depends(get_session)):
    new_product = Product.from_orm(product_data)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product
