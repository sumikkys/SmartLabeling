# project_schema.py
from pydantic import BaseModel
from typing import Optional

class ProjectRequest(BaseModel):
    project_name: str
    storage_path: Optional[str] = "F:/SmartLabeling/projects"  # 默认路径

class ProjectResponse(BaseModel):
    message: str
    project_path: str