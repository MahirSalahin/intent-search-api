from fastapi import APIRouter
from schemas.common import ResponseMessage
from utils.fetch_products import fetch_products

router = APIRouter(prefix="/query")


@router.post("/")
async def query_api(query: str):
    """
    Query the API with a given query string.

    Args:
        query (str): The query string to search for.

    Returns:
        ResponseMessage: The response message containing the results.
    """
    results = await fetch_products(query)
    return results
