from fastapi import APIRouter, UploadFile, File, HTTPException
from services.image_service import save_uploaded_image
from fastapi.responses import JSONResponse
from schemas.image_schema import*
from services.image_service import allowed_file, save_uploaded_file

router = APIRouter()

@router.post("/uploadimage", response_model=ImageResponse)
async def upload_image(image: UploadFile = File(...)):
    # 检查文件类型
    if not allowed_file(image.filename):
        raise HTTPException(status_code=415, detail="Unsupported media type. Only JPEG, PNG, and BMP files are allowed.")
    
    try:
        file_location = await save_uploaded_file(image, image.filename)

        return JSONResponse(
            content={
                "status": "success",
                "message": "Image uploaded successfully",
                "data": ImageResponseData(image_path=str(file_location))
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")