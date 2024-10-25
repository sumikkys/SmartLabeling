from pydantic import BaseModel
from typing import Optional

class ImageUploadResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict]