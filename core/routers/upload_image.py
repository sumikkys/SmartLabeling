from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from services.image_service import save_image_from_path
from schemas.image_schema import ImageResponse, ImageResponseData, ImageRequest

router = APIRouter()

@router.post("/uploadimage", response_model=ImageResponse)
async def upload_image(image: ImageRequest):
    """Rreceive an image from the client and save it to the server."""
    try:
        # Image save directory
        save_dir = "upload_images"
        file_location = save_image_from_path(image.image_path, save_dir)

        response_data = ImageResponse(
            status="success",
            message="Image uploaded successfully",
            data=ImageResponseData(image_path=file_location)
        )

        return response_data 
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
