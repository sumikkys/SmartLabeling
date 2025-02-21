# annotation_tools_schema.py
from pydantic import BaseModel
from typing import List, Optional


class MaskData(BaseModel):
    image_name: str
    class_id: int
    masks: List[List[int]]  


class UpdateMaskClassRequest(BaseModel):
    new_class_id: int


class AddClassRequest(BaseModel):
    class_name: str
    project_name: str
    project_path: Optional[str] = "F:/SmartLabeling/projects"  # 默认路径


class DeleteClassRequest(BaseModel):
    class_id: int
    project_name: str
    project_path: Optional[str] = "F:/SmartLabeling/projects"  # 默认路径


class ClassResponse(BaseModel):
    class_id: int
    class_name: str


class MaskResponse(BaseModel):
    mask_id: str
    class_id: int
    masks: List[List[int]]


class BaseResponse(BaseModel):
    message: str


class ClassListResponse(BaseResponse):
    classes: List[ClassResponse]


class MaskListResponse(BaseResponse):
    masks: List[MaskResponse]
