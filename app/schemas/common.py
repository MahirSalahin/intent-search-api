from pydantic import BaseModel
from typing import Any


class ResponseMessage(BaseModel):
    message: str
    status_code: int
    data: Any
    error: Any
