#export_service.py
import numpy as np
import yaml
from PIL import Image
from schemas.export_schema import ExportRequest
from typing import Dict
from pathlib import Path
from cache.image_cache import *
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
        classes = image_data_cache[image_id]["classes"]
    except KeyError:
        print(f"Image ID {image_id} not found in cache.")
        return yaml_path

    for class_id in classes:
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
    masks_path = Path(save_dir) / "masks" / f"{project_name}_exported_image.png"
    yaml_path = Path(save_dir) / f"{project_name}.yaml" 
    for image_id in request.image_id:
        try:
            data = image_data_cache[image_id]["masks"]
            image_width = image_data_cache[image_id]["width"]
            image_height = image_data_cache[image_id]["height"]
        except KeyError:
            print(f"Image ID {image_id} not found in cache.")
            continue

        # 创建灰度图像（单通道）
        mask_data = np.zeros((image_height, image_width), dtype=np.uint8)

        # 将标注数据转换为图像中的灰度值
        for class_id in data:
            masks = data[class_id]
            for annotation in masks.values():
                for y, row in enumerate(annotation):
                    for x, value in enumerate(row):
                        if value != 0.0:
                            if 0 <= x < image_width and 0 <= y < image_height:
                                mask_data[y, x] = class_id
        # 生成灰度图并保存
        image_mask = Image.fromarray(mask_data)
        try:
            image_mask.save(masks_path)
        except IOError as exc:
            print(f"Error saving image {masks_path}: {exc}")
            continue

        yaml_path = update_yaml(yaml_path, image_id)

    return {"masks_path": str(masks_path), "yaml_path": str(yaml_path)}