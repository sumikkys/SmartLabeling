# readProject.py
from fastapi import APIRouter, HTTPException
from schemas.project_schema import *
from services.project_service import read_project

router = APIRouter()

@router.post("/read-project", response_model=ProjectResponseforRead)
def readproject(request: ProjectRequestforRead):
    """读取项目"""
    project_name, cache_path = read_project(request)
    return ProjectResponseforRead(message="Project read successfully", project_name=project_name, cache_path=cache_path)
