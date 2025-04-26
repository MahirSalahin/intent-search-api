from fastapi import APIRouter
from schemas.product import Product
from schemas.common import ResponseMessage

router = APIRouter(prefix="/product")


@router.post("/", response_model=ResponseMessage)
async def get_products(product: Product):
    return ResponseMessage(
        message="Products fetched",
        status_code=200,
        data=product,
        error=None
    )
