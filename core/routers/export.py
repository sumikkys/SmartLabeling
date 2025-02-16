#export.py
from fastapi import APIRouter, HTTPException
from schemas.export_schema import ExportRequest, ExportResponse, ExportResponseData
from services.export_service import export_annotations

router = APIRouter()

@router.post("/export", response_model=ExportResponse)
async def export(request: ExportRequest):
    try:
        # 调用服务进行数据导出
        result = export_annotations(request)
        
        # 返回存储路径和状态
        response_data = ExportResponse(
            status = "success",
            message = "Export successful",
            data = ExportResponseData(masks_path= result["masks_path"], yaml_path= result["yaml_path"] )
        )

        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
