#export_service.py
import os
import numpy as np
import yaml
from PIL import Image
from schemas.export_schema import ExportRequest
from typing import Dict

def export_annotations(request: ExportRequest) -> Dict[str, str]:

    save_dir = "core/user/export_data"
    image_path = save_dir + "/" +"exported_image.png"
    yaml_path = save_dir + "/" + "annotations.yaml"

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
    image_mask.save(image_path)

    # 创建对应的YAML标注数据
    label = {"_background_": 0}
    for annotation in annotations:
        label[f"class{annotation.class_id}"] = annotation.class_id

    yaml_data = {
        "label names": label
    }

    with open(yaml_path, 'w') as yaml_file:
        yaml.dump(yaml_data, yaml_file, default_flow_style=False)

    # 返回文件路径
    return {"image_path": image_path, "yaml_path": yaml_path}
