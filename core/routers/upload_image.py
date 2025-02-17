# upload_image.py
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from services.image_service import save_image_from_path
from schemas.image_schema import ImageResponse, ImageResponseData, ImageRequest
from cache.image_embeddings_cache import *
from initialize_model import encoder
from pathlib import Path
import os
import cv2

router = APIRouter()

@router.post("/uploadimage", response_model=ImageResponse)
async def upload_image(image: ImageRequest):
    """Rreceive an image from the client and save it to the server."""
    try:
        save_dir = Path(image.storage_path) / image.project_name / "images"
        file_location = save_image_from_path(image.image_path, save_dir)
        # 本地上传图片到项目内后，给目标图片初始化：设置id、类别、mask、宽高
        # 未设定id时 image_path是image的唯一标识符
        # 此处将image_path转换为image_id
        image_path = str(save_dir / os.path.basename(image.image_path))

        if image_path not in image_id_cache:
            image_id_cache[image_path] = len(image_id_cache)
        image_id = image_id_cache[image_path]

        img_file = cv2.imread(image_path)
        height, width, _ = img_file.shape
        image_data_cache[image_id] = {
            "classes": {0: "_background_"},
            "masks": [[]],
            "width": width,
            "height": height
        }

        if image_id in image_embeddings_cache:
            img_embeddings = image_embeddings_cache[image_id]
        else:
            img_embeddings = encoder(img_file)  #无记录则调用encoder生成img_embeddings
            image_embeddings_cache[image_id] = img_embeddings

        response_data = ImageResponse(
            status="success",
            message="Image uploaded successfully",
            image_data = image_data_cache[image_id],#测试版本保留
            data=ImageResponseData(image_path=file_location, storage_path=str(save_dir))
        )

        return response_data 
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
