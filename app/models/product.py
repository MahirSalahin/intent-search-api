from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class Products(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    specTableContent: str
    category: str
    brand: str
    price: float