from fastapi import APIRouter
from models.product import Products
from schemas.common import ResponseMessage

router = APIRouter(prefix="/product")


@router.post("/", response_model=ResponseMessage)
async def get_products(product: Products):
    return ResponseMessage(
        message="Products fetched",
        status_code=200,
        data=product,
        error=None
    )
