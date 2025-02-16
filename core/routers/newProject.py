# newProject.py
from fastapi import APIRouter, HTTPException
from schemas.project_schema import ProjectRequest, ProjectResponse
from services.project_service import create_project_dir

router = APIRouter()

@router.post("/create-project", response_model=ProjectResponse)
async def create_project(request: ProjectRequest):
    """创建新项目"""
    result = create_project_dir(request)

    if "Error" in result:
        raise HTTPException(status_code=400, detail=result)

    return ProjectResponse(message="Project created successfully", project_path=result)
