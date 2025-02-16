# image_schema.py
from pydantic import BaseModel

class ImageResponseData(BaseModel):
    image_path: str 

class ImageResponse(BaseModel):
    status: str
    message: str
    data: ImageResponseData
    
class ImageRequest(BaseModel):
    image_path: str 