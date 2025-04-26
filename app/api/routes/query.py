from fastapi import APIRouter


router = APIRouter(prefix="/query")


@router.post("/")
async def query_api(query: str):
    pass        
