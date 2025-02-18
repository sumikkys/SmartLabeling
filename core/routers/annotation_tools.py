# annotation_tools.py
from fastapi import APIRouter, HTTPException
from schemas.annotation_tools_schema import MaskData, UpdateMaskClassRequest, AddClassRequest, DeleteClassRequest
from services.annotation_tools_service import AnnotationService, ClassResponse, MaskResponse
from cache.image_cache import *
from pathlib import Path

router = APIRouter()
annotation_service = AnnotationService()

@router.post("/add_mask")
async def add_mask(mask_data: MaskData):
    """标注一个新的 Mask"""
    mask = annotation_service.add_mask(mask_data)
    if mask is None:
        raise HTTPException(status_code=400, detail="No image selected")
    return {"message": "Mask added successfully", "mask": mask}


@router.delete("/delete_mask/{mask_id}")
async def delete_mask(mask_id: str):
    """删除已标注的 Mask"""
    annotation_service.delete_mask(mask_id)
    return {"message": "Mask deleted successfully"}


@router.put("/update_mask_class/{mask_id}")
async def update_mask_class(mask_id: str, update_data: UpdateMaskClassRequest):
    """更改已标注的 Mask 的 class"""
    mask = annotation_service.update_mask_class(mask_id, update_data.new_class_id)
    if mask is None:
        raise HTTPException(status_code=404, detail="Mask not found")
    return {"message": "Mask class updated", "mask": mask}


@router.get("/classes")
async def get_classes():
    """返回目前项目所有的 classes"""
    classes = annotation_service.get_classes()
    if not classes:
        raise HTTPException(status_code=400, detail="No image selected or no classes defined")
    return {"classes": classes}


@router.post("/add_class")
async def add_class(class_data: AddClassRequest):
    """为当前项目添加 class"""
    annotation_service.add_class(class_data.class_name)
    classes = annotation_service.get_classes()
    return {"message": "Class added successfully", "classes": classes}


@router.delete("/delete_class/{class_id}")
async def delete_class(class_id: int):
    """删除 class"""
    result = annotation_service.delete_class(class_id)
    if result.startswith("Cannot"):
        raise HTTPException(status_code=400, detail=result)
    classes = annotation_service.get_classes()
    return {"message": "Class deleted successfully", "classes": classes}
