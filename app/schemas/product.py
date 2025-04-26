from pydantic import BaseModel


class Product(BaseModel):
    id: int
    title: str
    description: str
    spec_table_content: str
    cluster_id: int
    category: str
    category_alt: str
    brand: str
    brand_alt: str
    price: float
    price_alt: float
