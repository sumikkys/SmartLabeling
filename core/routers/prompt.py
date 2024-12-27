# prompt.py
from fastapi import APIRouter, HTTPException
from schemas.prompt_schema import PromptRequest, PromptResponse
from services.prompt_service import process_prompt
from initialize_model import encoder
import cv2
import logging

# ≈‰÷√»’÷æº«¬º
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
        
        image_path = "images/test_image.png"
        logger.info("Reading image from path: %s", image_path)
        img_file = cv2.imread(image_path)
        
        if img_file is None:
            logger.error("Image not found at path: %s", image_path)
            raise ValueError(f"Image not found at path: {image_path}")
        
        logger.info("Image read successfully, processing with encoder")
        img_embeddings = encoder(img_file)
        
        logger.info("Image embeddings generated, processing prompt")
        response_data = process_prompt(request, img_embeddings, img_file)
        
        logger.info("Prompt processed successfully, returning response")
        return response_data
    except Exception as e:
        logger.error(f"Error processing prompt: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")