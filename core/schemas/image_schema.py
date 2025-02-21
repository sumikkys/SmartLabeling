# image_schema.py
from pydantic import BaseModel
from typing import Optional

class ImageResponseData(BaseModel):
    image_path: str
    image_name : str

class ImageResponse(BaseModel):
    status: str
    message: str
    image_data: dict #测试版本保留
    data: ImageResponseData
    
class ImageUploadRequest(BaseModel):
    image_path: str # 用户上传的图片原始路径
    project_name: str
    storage_path: Optional[str] = "F:/SmartLabeling/projects"  # 默认路径 

class ProjectImageRequest(BaseModel):
    image_name: str
    project_name: str
    project_path: Optional[str] = "F:/SmartLabeling/projects"  # 默认路径

