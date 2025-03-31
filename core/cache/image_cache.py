# # image_cache.py
import numpy as np
from typing import Dict, Any

class ImageCache:
    """图像缓存管理类"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.image_id_cache: Dict[str, str] = {}
            self.image_data_cache: Dict[str, Dict] = {}
            self.image_class_cache: Dict[int, str] = {0: "_background_"}
            self.image_embeddings_cache: Dict[int, np.ndarray] = {}
            self.current_image_id: str = "0"
            self._initialized = True

    def reset(self):
        """重置所有缓存数据"""
        self.__init__()

    def set_current_id(self, image_id: str):
        """设置当前图像ID"""
        self.current_image_id = image_id
    
    def get_current_id(self) -> str:
        """获取当前图像ID"""
        return self.current_image_id

    def find_key_by_value(self, dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key
        return None

# 创建全局单例实例
cache_manager = ImageCache()

# # 添加一个字典来存储每张图对应的img_embeddings
# # 后期可以做个导出工作从本地文件中读取
# # 或者用redis存储，故模块化
# # key -> value
# image_id_cache = {} # image_path -> image_id
# # (唯一)class_id
# # (唯一)mask_id = str(mask_data.class_id) + "_" +str(len(image_data_cache[image_id].masks[mask_data.class_id]))
# image_data_cache = {} # image_id -> image_data (classes, masks, width, height)
# # image_data_cache = {
# #     1: {
# #         "masks": {
# #                 0:{
# #                     "0_0": [[]],
# #                   },
# #                 1:{
# #                     "1_0": [[]],
# #                   },
# #                 2:{
# #                     "2_0": [[]],    
# #                   }
# #                 },
# #         "width": 1024,
# #         "height": 768
# #     }
# #     2: {}
# # }
# image_class_cache = {} # class_id -> class_name
# # image_class_cache = {
# #     0: "_background_",
# #     1: "class1",
# #     2: "class2"
# # }
# image_embeddings_cache = {} # image_id -> img_embeddings
# current_image_id = 0
# def get_current_id():
#     global current_id
#     return current_id

# def set_current_id(new_id):
#     global current_id
#     current_id = new_id
# # 用于字典的反向查找
# def find_key_by_value(dictionary, value):
#     for key, val in dictionary.items():
#         if val == value:
#             return key
#     return None