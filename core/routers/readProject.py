# readProject.py
from fastapi import APIRouter, HTTPException
from schemas.project_schema import ProjectRequest, ProjectResponse
from services.project_service import read_project

router = APIRouter()

@router.post("/read-project", response_model=ProjectResponse)
def readproject(request: ProjectRequest):
    """读取项目"""
    project_path = read_project(request)
    if not project_path:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse(message="Project read successfully", project_path=project_path)
