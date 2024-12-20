from pydantic import BaseModel
from pathlib import Path

# �����ϴ��ļ���Ŀ¼
UPLOAD_DIR = Path("uploaded_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ���������ϴ����ļ���ʽ
ALLOWED_EXTENSIONS = {'jpeg', 'png', 'bmp'}

class ImageResponseData(BaseModel):
    image_path: str

class ImageResponse(BaseModel):
    status: str
    message: str
    data: ImageResponseData
