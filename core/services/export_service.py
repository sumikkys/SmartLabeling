#export_service.py
import os
import numpy as np
import yaml
from PIL import Image
from schemas.export_schema import ExportRequest
from typing import Dict
from pathlib import Path

def update_yaml(yaml_path: str, annotations: list):
    try:
        with open(yaml_path, 'r') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
    except FileNotFoundError:
        yaml_data = {"label_names": {"_background_": 0}}

    label = yaml_data["label_names"]

    for annotation in annotations:
        class_name = f"class{annotation.class_id}"
        if class_name not in label:
            label[class_name] = annotation.class_id

    yaml_data["label_names"] = label

    with open(yaml_path, 'w') as yaml_file:
        yaml.dump(yaml_data, yaml_file, default_flow_style=False)

    return str(yaml_path)

def export_annotations(request: ExportRequest) -> Dict[str, str]:
    project_name = request.project_name
    save_dir = Path(request.project_path) / project_name
    masks_path = Path(save_dir) / "masks" / f"{project_name}_exported_image.png"
    yaml_path = Path(save_dir) / f"{project_name}.yaml" 

    annotations = request.annotations
    image_width = request.image_width
    image_height = request.image_height

    # 创建灰度图像（单通道）
    mask_data = np.zeros((image_height, image_width), dtype=np.uint8)

    # 将标注数据转换为图像中的灰度值
    for annotation in annotations:
        class_id = annotation.class_id
        for y, row in enumerate(annotation.masks):
            for x, value in enumerate(row):
                if value != 0.0:
                    if 0 <= x < image_width and 0 <= y < image_height:
                        mask_data[y, x] = class_id
    # 生成灰度图并保存
    image_mask = Image.fromarray(mask_data)
    image_mask.save(masks_path)

    yaml_path = update_yaml(yaml_path, annotations)

    return {"masks_path": str(masks_path), "yaml_path": str(yaml_path)}