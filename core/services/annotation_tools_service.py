# annotation_tools_service.py
from typing import List, Optional
from schemas.annotation_tools_schema import *


class AnnotationService:
    def __init__(self):
        # 存储每个 image_name 对应的 classes 和 masks
        self.images_data = {}
        self.current_image_id = None  # 当前图片的 ID

    def get_classes(self) -> List[ClassResponse]:
        """获取当前图片所有类别"""
        if self.current_image_id is None:
            return []
        return [
            ClassResponse(class_id=k, class_name=v)
            for k, v in self.images_data[self.current_image_id]['classes'].items()
        ]

    def add_class(self, class_name: str) -> None:
        """添加新类别"""
        if self.current_image_id is None:
            return
        new_class_id = max(self.images_data[self.current_image_id]['classes'].keys()) + 1
        self.images_data[self.current_image_id]['classes'][new_class_id] = class_name

    def delete_class(self, class_id: int) -> str:
        """删除类别"""
        if self.current_image_id is None:
            return "No image selected"

        if any(mask.class_id == class_id for mask in self.images_data[self.current_image_id]['masks'].values()):
            return "Cannot delete class, there are masks using it."
        
        del self.images_data[self.current_image_id]['classes'][class_id]
        return "Class deleted successfully"

    def switch_image(self, image_name: str) -> str:
        """切换图片"""
        self.current_image_id = image_name
        if image_name not in self.images_data:
            # 初始化新图片的数据
            self.images_data[image_name] = {
                "classes": {0: "_background_"},  # 默认只有背景类
                "masks": {}
            }
        return f"Switched to image: {image_name}"

    def add_mask(self, mask_data: MaskData) -> MaskResponse:
        """添加一个新的标注 Mask"""
        if self.current_image_id is None:
            return None
        mask_id = str(len(self.images_data[self.current_image_id]['masks']) + 1)
        self.images_data[self.current_image_id]['masks'][mask_id] = mask_data
        return MaskResponse(mask_id=mask_id, class_id=mask_data.class_id, coordinates=mask_data.coordinates)

    def delete_mask(self, mask_id: str) -> None:
        """删除标注的 Mask"""
        if self.current_image_id is None:
            return
        if mask_id in self.images_data[self.current_image_id]['masks']:
            del self.images_data[self.current_image_id]['masks'][mask_id]

    def update_mask_class(self, mask_id: str, new_class_id: int) -> Optional[MaskResponse]:
        """更新已标注 Mask 的类别"""
        if self.current_image_id is None:
            return None
        if mask_id in self.images_data[self.current_image_id]['masks']:
            self.images_data[self.current_image_id]['masks'][mask_id].class_id = new_class_id
            return MaskResponse(mask_id=mask_id, class_id=new_class_id, coordinates=self.images_data[self.current_image_id]['masks'][mask_id].coordinates)
        return None
