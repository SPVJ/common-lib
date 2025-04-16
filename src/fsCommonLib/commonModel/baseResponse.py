from typing import Optional
from pydantic import BaseModel

class BaseResponse(BaseModel):
    status: str
    code: str
    desc: Optional[str] = None