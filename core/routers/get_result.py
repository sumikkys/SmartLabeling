from fastapi import APIRouter, HTTPException
from services.result_service import get_segmentation_result

router = APIRouter()

@router.get("/getresult/{result_id}")
async def get_result(result_id: str):
    try:
        result = get_segmentation_result(result_id)
        if not result:
            raise HTTPException(status_code=404, detail="Segmentation result not found")
        return {
            "status": "success",
            "message": "Segmentation result retrieved successfully",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
