# annotation_tools.py
from fastapi import APIRouter, HTTPException
from schemas.annotation_tools_schema import *
from services.annotation_tools_service import process_prompt

router = APIRouter()

@router.post("/prompt", response_model=PromptResponse)

async def annotation_prompt(request: PromptRequest):
    try:
        response_data = process_prompt(request)
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")