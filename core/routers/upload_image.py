from fastapi import APIRouter, UploadFile, File, HTTPException
from services.image_service import save_image

router = APIRouter()

@router.post("/uploadimage")
async def upload_image(image: UploadFile = File(...)):
    try:
        processed_image_path = save_image(image)
        return {
            "status": "success",
            "message": "Image uploaded and processed successfully",
            "data": {
                "image_path": processed_image_path
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
