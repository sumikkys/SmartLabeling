import shutil
import os
from fastapi import UploadFile
from schemas.image_schema import ImageUploadResponse

def save_uploaded_image(image: UploadFile) -> ImageUploadResponse:
    try:    
        save_path = f"./uploaded_images/{image.filename}"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        # 假设处理图像并返回结果路径
        processed_image_path = f"/path/to/processed_image.jpg"
        
        return ImageUploadResponse(
            status="success",
            message="Image uploaded and processed successfully",
            data={"image_path": processed_image_path}
        )
    except Exception as e:
        return ImageUploadResponse(
            status="error",
            message=str(e),
            data=None
        )


