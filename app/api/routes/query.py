from fastapi import APIRouter
from utils.fetch_products import fetch_products
from crud.product import find_products_by_ids
from api.deps import SessionDep

router = APIRouter(prefix="/query")


@router.get("/")
async def query_api(query: str, db: SessionDep):
    """
    Query the API with a given query string.

    Args:
        query (str): The query string to search for.

    Returns:
        List of products matching the query intent.
    """
    product_ids, filter = await fetch_products(query)

    products = find_products_by_ids(db, product_ids)

    return {
        "message" : "Successfully fetched products",
        "status_code" : 200,
        "filter" : filter,
        "data" : products,
        "error" : None
    }
