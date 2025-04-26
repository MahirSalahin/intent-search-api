from fastapi import APIRouter, Query
from utils.fetch_products import fetch_products
from crud.product import find_products_by_ids, fuzzy_search_products
from api.deps import SessionDep
from crud.product import find_products_by_ids
from api.deps import SessionDep

router = APIRouter(prefix="/query")


@router.get("/")
async def query_api(query: str, db: SessionDep):
@router.get("/")
async def query_api(query: str = Query(..., description="The search query"), 
                   db: SessionDep = None):
    """
    Query the API with a given query string.

    Args:
        query (str): The query string to search for.
        db (Session): Database session dependency.

    Returns:
        List of products matching the query intent.
    """
    product_ids = await fetch_products(query)

    products = find_products_by_ids(db, product_ids)

    return ResponseMessage(
        message="Successfully fetched products",
        status_code=200,
        data=products,
        error=None
    )
        List of products matching the query intent.
    """
    # Try semantic search first
    response = await fetch_products(query)
    
    # If semantic search returns no results, fall back to fuzzy search
    if not response:
        products = fuzzy_search_products(db, query)
        return {
            "message": "Falling back to fuzzy search",
            "status_code": 200,
            "search_type": "fuzzy",
            "data": products,
            "error": None
        }
        
    # Otherwise, use semantic search results
    product_ids, filter = response
    products = find_products_by_ids(db, product_ids)

    return {
        "message": "Successfully fetched products by semantic search",
        "status_code": 200,
        "search_type": "semantic",
        "filter": filter,
        "data": products,
        "error": None
    }
