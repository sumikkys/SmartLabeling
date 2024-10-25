from fastapi import APIRouter, HTTPException
from schemas.prompt_schema import PromptRequest, PromptResponse
from services.prompt_service import process_prompt

router = APIRouter()

@router.post("/prompt", response_model=PromptResponse)
async def prompt(request: PromptRequest):
    global decoder, img_embeddings, img_file
    try:
        response_data = process_prompt(request, decoder, img_embeddings, img_file)
        return PromptResponse(status="success", message="Operation completed", data=response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
