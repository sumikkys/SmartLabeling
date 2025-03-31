# export_schema.py
from pydantic import BaseModel
from typing import List , Optional

class ExportResponseData(BaseModel):
    masks_path: str
    yaml_path: str
    cache_path: str

class ExportResponse(BaseModel):
    status: str
    message: str
    data: ExportResponseData
    
class ExportRequest(BaseModel):
    image_id: List[str]
    project_name: str
    # project_path: Optional[str] = "F:/SmartLabeling/projects"  # 默认路径
    project_path: Optional[str] = "/Users/alexemarie/Documents/SmartLabeling/projects"  # 默认类型