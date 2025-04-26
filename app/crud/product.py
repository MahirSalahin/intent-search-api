from sqlmodel import Session, select
from models.product import Products
from typing import List


def find_products_by_ids(db: Session, product_ids: List[int]) -> List[Products]:
    """
    Get multiple products by their IDs in a single database query

    Args:
        db: Database session
        product_ids: List of product IDs to fetch

    Returns:
        List of Products matching the provided IDs
    """
    if not product_ids:
        return []

    statement = select(Products).where(Products.id.in_(product_ids))
    results = db.exec(statement).all()

    return results
