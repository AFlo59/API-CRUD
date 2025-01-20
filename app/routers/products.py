from fastapi import APIRouter, Depends, Query, HTTPException, status, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from app.database import get_session
from app.models import Product, ProductCreate
from app.auth.auth import get_current_user
from typing import List, Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")  # Configurer les templates HTML

# Lister tous les produits
@router.get("/", response_model=List[Product], summary="Lister les produits")
async def list_products(session: Session = Depends(get_session), user=Depends(get_current_user)):
    """
    Retourne la liste complète des produits.
    """
    statement = select(Product)
    products = session.exec(statement).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun produit trouvé")
    return products


# Créer un produit via API
@router.post("/", response_model=Product, summary="Créer un produit")
async def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    """
    Crée un nouveau produit dans la base de données.
    """
    try:
        new_product = Product(**product.dict(exclude_unset=True))
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        return new_product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du produit : {str(e)}"
        )


# Formulaire pour créer un produit
@router.get("/create", response_class=HTMLResponse, summary="Créer un produit via formulaire")
async def create_product_form(request: Request):
    """
    Affiche un formulaire HTML pour créer un produit.
    """
    return templates.TemplateResponse("create_product.html", {"request": request})


# Créer un produit via formulaire HTML
@router.post("/create", response_class=HTMLResponse, summary="Créer un produit via formulaire")
async def create_product_via_form(
    request: Request, 
    name: str = Form(...), 
    product_number: str = Form(...), 
    color: Optional[str] = Form(None), 
    list_price: Optional[float] = Form(None),
    session: Session = Depends(get_session)
):
    """
    Crée un produit via un formulaire HTML.
    """
    try:
        new_product = Product(
            Name=name,
            ProductNumber=product_number,
            Color=color,
            ListPrice=list_price
        )
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        return HTMLResponse(f"<h1>Produit '{new_product.Name}' créé avec succès !</h1>")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création via formulaire : {str(e)}"
        )


# Mettre à jour un produit
@router.put("/{product_id}", response_model=Product, summary="Mettre à jour un produit")
async def update_product(
    product_id: int, 
    product: ProductCreate, 
    session: Session = Depends(get_session), 
    user=Depends(get_current_user)
):
    """
    Met à jour un produit existant dans la base de données.
    """
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
@router.delete("/{product_id}", summary="Supprimer un produit")
async def delete_product(product_id: int, session: Session = Depends(get_session), user=Depends(get_current_user)):
    """
    Supprime un produit de la base de données.
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit non trouvé")
    
    session.delete(product)
    session.commit()
    return {"message": f"Produit {product_id} supprimé avec succès"}


# Recherche dynamique par critères
@router.get("/search", response_model=List[Product], summary="Rechercher des produits dynamiquement")
async def search_products(
    name: Optional[str] = Query(None, description="Nom ou partie du nom du produit"),
    color: Optional[str] = Query(None, description="Couleur du produit"),
    size: Optional[str] = Query(None, description="Taille du produit"),
    min_price: Optional[float] = Query(None, description="Prix minimum"),
    max_price: Optional[float] = Query(None, description="Prix maximum"),
    session: Session = Depends(get_session),
):
    """
    Recherche dynamique de produits en fonction des critères fournis.
    """
    statement = select(Product)

    # Ajout des filtres dynamiquement
    if name:
        statement = statement.where(Product.Name.ilike(f"%{name}%"))
    if color:
        statement = statement.where(Product.Color.ilike(f"%{color}%"))
    if size:
        statement = statement.where(Product.Size == size)
    if min_price is not None:
        statement = statement.where(Product.ListPrice >= min_price)
    if max_price is not None:
        statement = statement.where(Product.ListPrice <= max_price)

    products = session.exec(statement).all()

    # Retourner une erreur si aucun produit n'est trouvé
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aucun produit trouvé avec les critères spécifiés"
        )

    return products


# Formulaire HTML pour rechercher un produit
@router.get("/search/form", response_class=HTMLResponse, summary="Formulaire de recherche de produits")
async def search_product_form(request: Request):
    """
    Affiche un formulaire HTML pour rechercher un produit.
    """
    return templates.TemplateResponse("search_product.html", {"request": request})
