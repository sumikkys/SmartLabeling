# switch_image.py
from fastapi import APIRouter, HTTPException
from schemas.image_schema import *
from services.image_service import switch_image
from cache.image_cache import image_id_cache
from pathlib import Path

router = APIRouter()

@router.post("/switch_image")
async def switchImage(image_request: ProjectImageRequest):
    """切换图片"""
    try:
        # 规范化项目路径和图像名称
        image_path = Path(image_request.project_path).expanduser().resolve() / image_request.project_name / "images" / image_request.image_name
        
        # 确保 image_path 是字符串
        image_path_str = str(image_path)
        
        # 获取 image_id
        image_id = image_id_cache.get(image_path_str)
        if image_id is None:
            raise ValueError(f"Image path {image_path_str} not found in cache.")
        image_name, image_data = switch_image(image_id)
        response_data = ImageResponse(
            status="success",
            message="Image switch successfully",
            image_data=image_data,
            data=ImageResponseData(image_path=image_path_str, image_name=image_name)
        )
        return response_data
    
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except KeyError as ke:
        raise HTTPException(status_code=404, detail=f"Image ID {image_id} not found in cache.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")