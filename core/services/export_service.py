#export_service.py
import numpy as np
import yaml
from PIL import Image
from schemas.export_schema import ExportRequest
from typing import Dict
from pathlib import Path
import json
from cache.image_cache import *
import os

def update_yaml(yaml_path: str, image_id: int) -> str:
    try:
        with open(yaml_path, 'r') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
    except FileNotFoundError:
        yaml_data = {"label_names": {"_background_": 0}}
    except yaml.YAMLError as exc:
        print(f"Error reading YAML file {yaml_path}: {exc}")
        return yaml_path

    label = yaml_data["label_names"]
    try:
        classes = image_class_cache
    except KeyError:
        print(f"Image ID {image_id} not found in cache.")
        return yaml_path

    for class_id in classes.keys():
        class_name = classes[class_id]
        if class_name not in label:
            label[class_name] = class_id

    yaml_data["label_names"] = label

    try:
        with open(yaml_path, 'w') as yaml_file:
            yaml.dump(yaml_data, yaml_file, default_flow_style=False)
    except yaml.YAMLError as exc:
        print(f"Error writing YAML file {yaml_path}: {exc}")

    return str(yaml_path)
def export_annotations(request: ExportRequest) -> Dict[str, str]:
    project_name = request.project_name
    save_dir = Path(request.project_path) / project_name
    
    if not save_dir.exists():
        raise FileNotFoundError(f"Project directory {save_dir} does not exist")
    
    results = []
    yaml_path = Path(save_dir) / f"{project_name}.yaml"
    
    # 过滤有效的 image_id
    valid_image_ids = []
    for image_id in request.image_id:
        if image_id not in image_data_cache:
            print(f"Skipping invalid Image ID {image_id}: Not found in cache.")
            continue
        valid_image_ids.append(image_id)
    
    if not valid_image_ids:
        raise Exception("No valid image IDs found in the request.")
    
    for image_id in valid_image_ids:
        try:
            # 为每个image_id创建唯一的文件名
            masks_path = Path(save_dir) / "masks" / f"{project_name}_{image_id}_exported.png"
            
            # 获取数据
            data = image_data_cache[image_id]["masks"]
            image_width = image_data_cache[image_id]["width"]
            image_height = image_data_cache[image_id]["height"]
            
            # 创建mask数据
            mask_data = np.zeros((image_height, image_width), dtype=np.uint8)
            
            # 转换标注数据
            for class_id in data.keys():
                masks = data[class_id]
                for annotation in masks.values():
                    for y, row in enumerate(annotation):
                        for x, value in enumerate(row):
                            if value != 0.0 and 0 <= x < image_width and 0 <= y < image_height:
                                mask_data[y, x] = 256 - class_id #反向导出灰度方便调试
            
            # 保存mask图像
            image_mask = Image.fromarray(mask_data)
            masks_path.parent.mkdir(parents=True, exist_ok=True)
            image_mask.save(masks_path)
            
            # 更新YAML文件
            update_yaml(str(yaml_path), image_id)
            
            results.append({
                "masks_path": str(masks_path),
                "yaml_path": str(yaml_path)
            })
            
        except (IOError, OSError) as e:
            print(f"Error saving files for image {image_id}: {e}")
        except Exception as e:
            print(f"Unexpected error processing image {image_id}: {e}")
    
    if not results:
        raise Exception("No annotations were successfully exported")
        
    # 返回最后一个成功的结果
    return results[-1]

def export_cache(request: ExportRequest) -> str:
    cache_path = Path(request.project_path) / request.project_name / "cache.json"
    if cache_path.exists():
        os.remove(cache_path)
    data = {
        "image_id_cache": image_id_cache,
        "image_data_cache": image_data_cache,
        "image_class_cache": image_class_cache,
        "image_embeddings_cache": {k: v.tolist() for k, v in image_embeddings_cache.items()},
        "current_image_id": current_image_id
    }
    with open(cache_path, 'w') as f:
        json.dump(data, f, indent=4)
    return str(cache_path)