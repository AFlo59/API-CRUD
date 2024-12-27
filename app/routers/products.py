from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models import Product, ProductCreate
from app.auth.auth import get_current_user
from typing import List

router = APIRouter()

# Lister les produits
@router.get("/", response_model=List[Product], summary="Lister les produits")
async def list_products(session: Session = Depends(get_session), user=Depends(get_current_user)):
    statement = select(Product)
    products = session.exec(statement).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun produit trouvé")
    return products

# Créer un produit
@router.post("/", response_model=Product, summary="Créer un produit")
async def create_product(product: ProductCreate, session: Session = Depends(get_session), user=Depends(get_current_user)):
    new_product = Product.from_orm(product)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

# Mettre à jour un produit
@router.put("/{product_id}", response_model=Product, summary="Mettre à jour un produit")
async def update_product(product_id: int, product: ProductCreate, session: Session = Depends(get_session), user=Depends(get_current_user)):
    existing_product = session.get(Product, product_id)
    if not existing_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit non trouvé")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(existing_product, key, value)
    session.add(existing_product)
    session.commit()
    session.refresh(existing_product)
    return existing_product

# Supprimer un produit
@router.delete("/{product_id}", response_model=dict, summary="Supprimer un produit")
async def delete_product(product_id: int, session: Session = Depends(get_session), user=Depends(get_current_user)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit non trouvé")
    session.delete(product)
    session.commit()
    return {"message": f"Produit {product_id} supprimé avec succès"}
