# upload_image.py
from fastapi import APIRouter, HTTPException
from services.image_service import save_image_from_path
from schemas.image_schema import ImageResponse, ImageResponseData, ImageUploadRequest
from cache.image_cache import *
from initialize_model import encoder
from pathlib import Path
import os
import cv2

router = APIRouter()

@router.post("/uploadimage", response_model=ImageResponse)
async def upload_image(image: ImageUploadRequest):
    """Receive an image from the client and save it to the server."""
    try:
        # 规范化存储路径和项目路径
        save_dir = Path(image.storage_path).expanduser().resolve()/ image.project_name / "images"
        image_path = Path(image.image_path).expanduser().resolve()
        
        # 保存图像到指定路径
        saved_image_path = save_image_from_path(str(image_path), str(save_dir))
        
        # 规范化保存后的图像路径
        saved_image_path = Path(saved_image_path).expanduser().resolve()
        
        # 将路径转换为字符串
        saved_image_path_str = str(saved_image_path)
        
        # 本地上传图片到项目内后，给目标图片初始化：设置id、类别、mask、宽高 
        # 未设定id时 image_path是image的唯一标识符
        # 此处将image_path转换为image_id
        image_name = os.path.basename(saved_image_path_str)

        if saved_image_path_str not in image_id_cache:
            image_id_cache[saved_image_path_str] = len(image_id_cache)
        image_id = image_id_cache[saved_image_path_str]
        
        set_current_id(image_id)
        current_image_id = get_current_id()
        
        img_file = cv2.imread(saved_image_path_str)
        height, width, _ = img_file.shape
        image_data_cache[current_image_id] = {
            "masks": {},
            "width": width,
            "height": height
        }

        if current_image_id in image_embeddings_cache:
            img_embeddings = image_embeddings_cache[current_image_id]
        else:
            img_embeddings = encoder(img_file)  # 无记录则调用encoder生成img_embeddings
            image_embeddings_cache[current_image_id] = img_embeddings
        
        response_data = ImageResponse(
            status="success",
            message="Image uploaded successfully",
            image_data=image_data_cache[current_image_id],  # 测试版本保留
            data=ImageResponseData(image_path=saved_image_path_str, image_name=image_name)
        )

        return response_data 
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")