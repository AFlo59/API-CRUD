from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Product, ProductCreate, ProductRead
from app.auth.auth import get_current_user

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/", response_model=List[ProductRead])
def read_products(
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Lister tous les produits
    """
    statement = select(Product)
    products = session.exec(statement).all()
    return products

@router.get("/{product_id}", response_model=ProductRead)
def read_product(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Récupérer un produit spécifique
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit non trouvé")
    return product

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Créer un nouveau produit
    """
    new_product = Product.from_orm(product_data)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    product_data: ProductCreate,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Mettre à jour un produit
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit non trouvé")

    # Mise à jour des champs
    product.Name = product_data.Name
    product.ProductNumber = product_data.ProductNumber
    product.Color = product_data.Color
    product.StandardCost = product_data.StandardCost
    product.ListPrice = product_data.ListPrice
    product.SellStartDate = product_data.SellStartDate

    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Supprimer un produit
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit non trouvé")
    session.delete(product)
    session.commit()
    return {"detail": "Produit supprimé avec succès"}
