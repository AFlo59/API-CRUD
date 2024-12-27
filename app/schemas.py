from pydantic import BaseModel
from typing import Optional

class ProductBaseSchema(BaseModel):
    Name: str
    ProductNumber: str
    Color: Optional[str] = None
    StandardCost: Optional[float] = None
    ListPrice: Optional[float] = None
    Size: Optional[str] = None
    Weight: Optional[float] = None
    ProductCategoryID: Optional[int] = None
    ProductModelID: Optional[int] = None

class ProductCreateSchema(ProductBaseSchema):
    pass

class ProductResponseSchema(ProductBaseSchema):
    ProductID: int
