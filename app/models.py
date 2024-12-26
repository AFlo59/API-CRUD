from sqlmodel import SQLModel, Field
from typing import Optional

class ProductBase(SQLModel):
    Name: str
    ProductNumber: str
    Color: Optional[str] = None
    StandardCost: Optional[float] = None
    ListPrice: Optional[float] = None

class Product(ProductBase, table=True):
    ProductID: Optional[int] = Field(default=None, primary_key=True)

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    ProductID: int
