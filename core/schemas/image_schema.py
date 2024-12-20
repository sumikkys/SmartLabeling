from pydantic import BaseModel
from pathlib import Path

# 定义上传文件的目录
UPLOAD_DIR = Path("uploaded_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 定义允许上传的文件格式
ALLOWED_EXTENSIONS = {'jpeg', 'png', 'bmp'}

class ImageResponseData(BaseModel):
    image_path: str

class ImageResponse(BaseModel):
    status: str
    message: str
    data: ImageResponseData
