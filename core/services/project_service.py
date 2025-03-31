# project_service.py
import yaml
from pathlib import Path
from typing import Optional, Tuple
import logging
from schemas.project_schema import *
import json
import numpy as np
from cache.image_cache import image_id_cache, image_data_cache, image_class_cache, image_embeddings_cache, current_image_id

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
        project_json = project_path / "cache.json"
        create_project_yaml(project_yaml)
        create_project_cacheJson(project_json)
        
        global image_id_cache, image_data_cache, image_class_cache, image_embeddings_cache, current_image_id
        image_id_cache = {}
        image_data_cache = {}
        image_class_cache = {0: "_background_"}
        image_embeddings_cache = {}
        current_image_id = 0

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
        
def create_project_cacheJson(json_path: Path):
    """创建 cache.json 文件"""
    data = {
        "image_id_cache": {},
        "image_data_cache": {},
        "image_class_cache": {0: "_background_"},
        "image_embeddings_cache": {},
        "current_image_id": 0
    }

    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)


# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def read_project(request: ProjectRequestforRead) -> Tuple[str, str]:
    """读取已创建项目"""
    project_path = Path(request.project_path).resolve()
    project_name = project_path.name

    logging.info(f"Attempting to read project: {project_name}")
    
    # 检查项目目录是否存在
    if not project_path.exists():
        logging.error(f"Project directory does not exist: {project_path}")
        return f"Project {project_name} does not exist.", ""

    cache_path = project_path / "cache.json"

    # 检查缓存文件是否存在
    if not cache_path.exists():
        logging.error(f"Cache file does not exist: {cache_path}")
        return "", f"Cache file for project {project_name} does not exist."

    try:
        # 加载缓存文件内容
        logging.info(f"Loading cache file: {cache_path}")
        with open(cache_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 更新全局缓存变量
        global image_id_cache, image_data_cache, image_class_cache, image_embeddings_cache, current_image_id
        image_id_cache = data["image_id_cache"]
        image_data_cache = data["image_data_cache"]
        image_class_cache = data["image_class_cache"]
        image_embeddings_cache = {k: np.array(v) for k, v in data["image_embeddings_cache"].items()}
        current_image_id = data["current_image_id"]
        print(image_id_cache, image_data_cache, image_class_cache, image_embeddings_cache, current_image_id)

        logging.info("Global cache variables updated successfully.")
        
        # 返回规范化后的路径
        logging.info(f"Project read successfully: {project_name}")
        return str(project_name), str(cache_path.resolve())

    except KeyError as e:
        logging.error(f"Missing key in cache file: {e}")
        return "", f"Error reading cache file: Missing key {e}"
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error in cache file: {e}")
        return "", f"Error reading cache file: JSON decode error {e}"
    except Exception as e:
        logging.error(f"Unexpected error reading cache file: {e}")
        return "", f"Error reading cache file: {str(e)}"

    