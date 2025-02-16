# project_service.py
import yaml
from pathlib import Path
from typing import Optional
from schemas.project_schema import ProjectRequest

def create_project_dir(request:ProjectRequest) -> Optional[str]:
    """创建项目目录及相关文件"""
    project_name = request.project_name
    project_path = Path(request.storage_path) / project_name
    image_dir = project_path / "images"
    mask_dir = project_path / "masks"
    
    # 如果项目目录已经存在，则返回
    if project_path.exists():
        return f"Project {project_name} already exists."

    # 创建项目目录及子目录
    try:
        project_path.mkdir(parents=True)
        image_dir.mkdir()
        mask_dir.mkdir()

        # 创建 YAML 文件
        project_yaml = project_path / f"{project_name}.yaml"
        create_project_yaml(project_yaml)

        return str(project_path)

    except Exception as e:
        return f"Error creating project: {str(e)}"

def create_project_yaml(yaml_path: Path):
    """创建 project.yaml 文件"""
    data = {
        "label_names": {
            '_background_': 0,
        }
    }

    with open(yaml_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

