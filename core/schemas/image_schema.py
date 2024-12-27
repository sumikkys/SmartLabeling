from pydantic import BaseModel
from pathlib import Path

class ImageResponseData(BaseModel):
    image_path: str 

class ImageResponse(BaseModel):
    status: str
    message: str
    data: ImageResponseData
    
# 定义请求体的 Pydantic 模型
class ImageRequest(BaseModel):
    image_path: str  # 从请求体中接收路径字段