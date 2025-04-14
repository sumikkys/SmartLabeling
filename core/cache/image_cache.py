# image_cache.py
import numpy as np
from typing import Dict, Any

class ImageCache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.image_id_cache: Dict[str, str] = {} # image_path -> image_id
            # (唯一)class_id=str
            # (唯一)mask_id = str(mask_data.class_id) + "_" +str(len(image_data_cache[image_id].masks[mask_data.class_id]))
            
            self.image_data_cache: Dict[str, Dict] = {} # image_id -> image_data (classes, masks, width, height)
            # image_data_cache = {
            #     1: {
            #         "masks": {
            #                 0:{
            #                     "0_0": [[]],
            #                   },
            #                 1:{
            #                     "1_0": [[]],
            #                   },
            #                 2:{
            #                     "2_0": [[]],    
            #                   }
            #                 },
            #         "width": 1024,
            #         "height": 768
            #     }
            #     2: {}
            # }

            self.image_class_cache: Dict[str, str] = {"0": "_background_"} # class_id -> class_name
            # image_class_cache = {
            #     0: "_background_",
            #     1: "class1",
            #     2: "class2"
            # }

            self.image_embeddings_cache: Dict[str, np.ndarray] = {} # image_id -> img_embeddings
            self.classes_features_cache: np.ndarray = np.empty((512, 0))
            self.image_pre_features_cache: Dict[str, np.ndarray] = {}
            self.shape_dict_cache: Dict[str, dict] = {}
            self.current_image_id: str = "0"
            self._initialized = True

    def reset(self):
        self.__init__()

    def set_current_id(self, image_id: str):
        self.current_image_id = image_id
    
    def get_current_id(self) -> str:
        return self.current_image_id

    def find_key_by_value(self, dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key
        return None
    
cache_manager = ImageCache()