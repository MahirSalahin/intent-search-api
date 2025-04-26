from fastapi import FastAPI, Response
from api.routes.query import router as query_router
from api.routes.product import router as product_router

app = FastAPI()
app.include_router(query_router)
app.include_router(product_router)


@app.get("/")
def get_home() -> Response:
    """
    Return server status
    """
    return Response("Server is running")
