# prompt.py
from fastapi import APIRouter, HTTPException
from schemas.prompt_schema import PromptRequest, PromptResponse
from services.prompt_service import process_prompt
from cache.image_cache import cache_manager
from initialize_model import encoder
import cv2
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/prompt", response_model=PromptResponse)
async def prompt(request: PromptRequest):
    try:
        logger.info("Received request: %s", request)
    
        if encoder is None:
            logger.error("Encoder is not initialized")
            raise ValueError("Encoder is not initialized")

        image_path = Path(request.storage_path) / request.project_name / "images" / request.image_name
        image_path = str(image_path)
        logger.info("Reading image from path: %s", image_path)
        img_file = cv2.imread(image_path)

        if img_file is None:
            logger.error("Image not found at path: %s", image_path)
            raise ValueError(f"Image not found at path: {image_path}")
        # 同upload_image检查目标image的初始化
        if image_path not in cache_manager.image_id_cache:
            cache_manager.image_id_cache[image_path] = str(len(cache_manager.image_id_cache))

        image_id = cache_manager.image_id_cache[image_path]

        if image_id in cache_manager.image_embeddings_cache:
            logger.info("Using cached image embeddings for path: %s", image_path)
            img_embeddings = cache_manager.image_embeddings_cache[image_id]
        else:
            logger.info("Image read successfully, processing with sam_encoder")
            img_embeddings = encoder(img_file)  #无记录则调用encoder生成img_embeddings
            cache_manager.image_embeddings_cache[image_id] = img_embeddings

        if cache_manager.classes_features_cache.any():
            logger.info("Using cached classes features")
            classes_features = cache_manager.classes_features_cache
        else:
            logger.info("cached classes features not found")
            classes_features = None

        logger.info("Classses features generated, processing prompt")
        response_data = await process_prompt(request, img_embeddings, img_file, classes_features)
        
        logger.info("Prompt processed successfully, returning response")
        return response_data
    except Exception as e:
        logger.error(f"Error processing prompt: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")