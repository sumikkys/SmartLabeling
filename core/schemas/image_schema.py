# image_schema.py
from pydantic import BaseModel
from typing import Optional

class ImageResponseData(BaseModel):
    image_path: str
    storage_path : str

class ImageResponse(BaseModel):
    status: str
    message: str
    data: ImageResponseData
    
class ImageRequest(BaseModel):
    image_path: str
    project_name: str
    storage_path: Optional[str] = "F:/SmartLabeling/projects"  # 默认路径 