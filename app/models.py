from typing import Optional
from sqlmodel import SQLModel, Field

class ProductBase(SQLModel):
    Name: str
    ProductNumber: str
    Color: Optional[str] = None
    StandardCost: float
    ListPrice: float

    # Parfois, SellStartDate est de type datetime
    # Pour simplifier, on la laisse en str ou date
    SellStartDate: Optional[str] = None

class Product(ProductBase, table=True):
    __tablename__ = "Product"  # Nom de la table
    ProductID: Optional[int] = Field(default=None, primary_key=True)

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    ProductID: int
