from sqlmodel import Session, select, or_
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

    # Create a query that selects products where the ID is in the provided list
    statement = select(Products).where(Products.id.in_(product_ids))
    results = db.exec(statement).all()

    return results


def fuzzy_search_products(db: Session, search_term: str, limit: int = 20) -> List[Products]:
    """
    Perform a basic text search on product titles and descriptions
    
    Args:
        db: Database session
        search_term: Text to search for
        limit: Maximum number of results to return
        
    Returns:
        List of Products matching the search criteria
    """
    if not search_term or search_term.strip() == "":
        # Return empty list for empty search terms
        return []
    
    # Break search term into words for better matching
    search_words = search_term.lower().split()
    
    # Build conditions for each word to be contained in title or description
    conditions = []
    for word in search_words:
        if len(word) > 2:  # Only use words longer than 2 characters
            conditions.append(
                or_(
                    Products.title.ilike(f"%{word}%"),
                    Products.description.ilike(f"%{word}%")
                )
            )
    
    # If no valid search words, return empty list
    if not conditions:
        return []
    
    # Use AND condition to require all words to be present
    statement = select(Products)
    
    # Apply all conditions (AND logic)
    for condition in conditions:
        statement = statement.where(condition)
    
    # Limit results
    statement = statement.limit(limit)
    
    try:
        results = db.exec(statement).all()
        if results:
            return results
            
        # If no results with AND logic, try OR logic for broader matches
        statement = select(Products).where(
            or_(*[  # Combine all conditions with OR
                or_(
                    Products.title.ilike(f"%{word}%"),
                    Products.description.ilike(f"%{word}%")
                ) for word in search_words if len(word) > 2
            ])
        ).limit(limit)
        
        return db.exec(statement).all()
    except Exception as e:
        print(f"Error during text search: {e}")
        return []
