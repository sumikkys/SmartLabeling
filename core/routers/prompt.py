# prompt.py
from fastapi import APIRouter, HTTPException
from schemas.prompt_schema import PromptRequest, PromptResponse
from services.prompt_service import process_prompt
from initialize_models import encoder
import cv2

router = APIRouter()

@router.post("/prompt", response_model=PromptResponse)
async def prompt(request: PromptRequest):
    try:
        if encoder is None:
            raise ValueError("Encoder is not initialized")
        image_path = "images/amos_0006_90.png"
        img_file = cv2.imread(image_path)
        img_embeddings = encoder(img_file)
        response_data = process_prompt(request, img_embeddings, img_file)
        return PromptResponse(status="success", message="Operation completed", data=response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")