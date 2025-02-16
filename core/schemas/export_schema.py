# export_schema.py
from pydantic import BaseModel
from typing import List , Optional

class ExportResponseData(BaseModel):
    masks_path: str
    yaml_path: str

class ExportResponse(BaseModel):
    status: str
    message: str
    data: ExportResponseData

class Annotation(BaseModel):
    class_id: int
    masks: List[List[float]] 

class ExportRequest(BaseModel):
    annotations: List[Annotation]
    project_name: str
    project_path: Optional[str] = "F:/SmartLabeling/projects"  # 默认路径
    image_width: int
    image_height: int