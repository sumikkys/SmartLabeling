# annotation_tools_service.py
from cache.image_cache import *  
from schemas.annotation_tools_schema import *
from utils import normalize, softmax, top_k
import cv2
import numpy as np
from initialize_model import clip_text_encoder, clip_vision_encoder

# 在文件开头添加全局计数器
class GlobalCounter:
    def __init__(self):
        self.class_counter = 1  # 每个image_id对应一个class计数器
        self.mask_counter = {}   # 每个image_id的每个class_id对应一个mask计数器
    
    def get_next_class_id(self) -> int:
        next_id = self.class_counter
        self.class_counter += 1
        return next_id

    def get_next_mask_id(self, image_id: int, class_id: int) -> str:
        if image_id not in self.mask_counter:
            self.mask_counter[image_id] = {}
        if class_id not in self.mask_counter[image_id]:
            self.mask_counter[image_id][class_id] = 0
        
        next_id = self.mask_counter[image_id][class_id]
        self.mask_counter[image_id][class_id] += 1
        return f"{class_id}_{next_id}"
    
global_counter = GlobalCounter()

class AnnotationService:
    def __init__(self):
        global image_data_cache
    
    def add_mask_clip(self, image_id: int, mask_data: MaskData) -> MaskResponse:
        """使用CLIP添加一个新的标注 Mask"""
        classes = []
        for class_id, class_name in image_class_cache.items():
            classes.append(class_name)
        prefix = "a photo of a "
        texts = [prefix + class_name for class_name in classes]
        image_id = get_current_id()
        image_path = find_key_by_value(image_id_cache, image_id)
        image = cv2.imread(image_path)

        prompt = {
            'points': np.array([[[200,300]]]).astype(np.float32),# (1,1,2) 即 (batch_size, num_points, 2)
            'labels': np.ones((1,1),dtype=np.int32), # (1,1) 即 (batch_size, num_points) 现在只有标签为1的点
        }

        image_features = clip_vision_encoder(np.array(image), prompt)

        texts_features = clip_text_encoder(texts)

        # 对图像和文本特征进行归一化
        image_features_normalized = normalize(image_features)
        text_features_normalized = normalize(texts_features)
        # 计算相似度
        similarity = 100.0 * np.matmul(image_features_normalized, text_features_normalized.T)
        similarity_softmax = softmax(similarity, axis=1)
        values, indices = top_k(similarity_softmax, 3)
        print("\n相似度结果:")
        result = []
        for i, (val, idx) in enumerate(zip(values[0], indices[0])):
            result.append(texts[idx])
            print(f"排名 {i+1}: {texts[idx]} (相似度: {val:.4f})")

        
        if image_id not in image_data_cache:
            return False
        mask_id = global_counter.get_next_mask_id(image_id, mask_data.class_id)
        if image_data_cache[image_id]["masks"].get(mask_data.class_id) is None:
            image_data_cache[image_id]["masks"][mask_data.class_id] = {}  
        image_data_cache[image_id]["masks"][mask_data.class_id][mask_id] = mask_data.masks
        return MaskResponse(mask_id=mask_id, class_id=mask_data.class_id)

    def add_mask(self,image_id: int, mask_data: MaskData) -> MaskResponse:
        """添加一个新的标注 Mask"""
        if image_id not in image_data_cache:
            return False
        mask_id = global_counter.get_next_mask_id(image_id, mask_data.class_id)
        if image_data_cache[image_id]["masks"].get(mask_data.class_id) is None:
            image_data_cache[image_id]["masks"][mask_data.class_id] = {}  
        image_data_cache[image_id]["masks"][mask_data.class_id][mask_id] = mask_data.masks
        return MaskResponse(mask_id=mask_id, class_id=mask_data.class_id)

    def delete_mask(self, image_id: int, mask_id: str) -> Optional[MaskResponse]:
        """删除标注的 Mask"""
        if image_id not in image_data_cache:
            return MaskResponse(mask_id=mask_id, class_id=None, message="Image ID not found.")
        
        class_id = int(mask_id.split("_")[0])
        
        if class_id not in image_data_cache[image_id]["masks"]:
            return MaskResponse(mask_id=mask_id, class_id=class_id, message="Class ID not found in image.")
        
        if mask_id in image_data_cache[image_id]["masks"][class_id]:
            del image_data_cache[image_id]["masks"][class_id][mask_id]
            return MaskResponse(mask_id=mask_id, class_id=class_id, message="Mask deleted successfully.")
        else:
            return MaskResponse(mask_id=mask_id, class_id=class_id, message="Mask ID not found.")

    def update_class_name(self, class_id: int, class_name: str) -> Optional[ClassResponse]:
        """更新类别"""
        if class_id in image_class_cache:
            image_class_cache[class_id] = class_name
            return ClassResponse(class_id=class_id, class_name=class_name)
        return None

    def get_classes(self) -> List[ClassResponse]:
        """获取当前图片所有类别"""
        classes = []
        for class_id, class_name in image_class_cache.items():
            classes.append(ClassResponse(class_id=class_id, class_name=class_name))
        return classes

    def add_class(self, class_name: str) -> Optional[ClassResponse]:
        """添加新类别"""
        if class_name in image_class_cache.values():
            class_id = find_key_by_value(image_class_cache, class_name)
            return ClassResponse(class_id=class_id, class_name=class_name, message="Class already exists.")
        
        class_id = global_counter.get_next_class_id()
        image_class_cache[class_id] = class_name
        return ClassResponse(class_id=class_id, class_name=class_name, message="Class added successfully.")

    def delete_class(self, class_id: int) -> Optional[ClassResponse]:
        """删除类别"""
        if class_id in image_class_cache.keys():
            class_name = image_class_cache[class_id]
            del image_class_cache[class_id]
            # for image_id in image_data_cache.keys():
            #     if image_data_cache[image_id]["masks"][class_id] is not None:
            #         del image_data_cache[image_id]["masks"][class_id]
            return ClassResponse(class_id=class_id, class_name=class_name, message="Class deleted successfully.")
        else:
            return ClassResponse(class_id=class_id, class_name="None", message="Class not found.")

annotation_service = AnnotationService()

def process_prompt(request: PromptRequest) -> PromptResponse:
    """处理来自前端的标注请求"""
    
    image_id = get_current_id()
    
    if image_id not in image_data_cache:
        return PromptResponse(
            status="error",
            message=f"Image with ID {image_id} not found",
            data=None
        )
    
    if request.operation == 0:  # 添加标注 Mask
        mask_data = request.mask_data
        result = annotation_service.add_mask(image_id, mask_data)
        if result:
            return PromptResponse(
                status="success",
                message="Mask added successfully",
                mask_id=result.mask_id,
                class_id=result.class_id
            )
        else:
            return PromptResponse(
                status="error",
                message="Failed to add mask",
                data=None
            )

    elif request.operation == 1:  # 删除标注 Mask
        mask_id = request.mask_id
        result = annotation_service.delete_mask(image_id, mask_id)
        if result:
            return PromptResponse(
                status="success",
                message=f"Mask {mask_id} deleted successfully",
                data=None
            )
        else:
            return PromptResponse(
                status="error",
                message=f"Mask {mask_id} not found",
                data=None
            )

    elif request.operation == 2:  # 更新类别
        class_id = request.class_id_change
        class_name = request.class_name
        result = annotation_service.update_class_name(class_id, class_name)
        if result:
            return PromptResponse(
                status="success",
                message=f"updated class {class_id}:{class_name} successfully",
                class_id=class_id
            )
        else:
            return PromptResponse(
                status="error",
                message=f"class {class_name} not found",
                data=None
            )

    elif request.operation == 3:  # 获取当前类别
        classes = annotation_service.get_classes()
        return PromptResponse(
            status="success",
            message="Classes fetched successfully",
            classes=classes,
            data=None
        )

    elif request.operation == 4:  # 添加新类别
        class_name = request.class_name
        result = annotation_service.add_class(class_name)
        return PromptResponse(
            status="success",
            message=f"Class '{class_name}' added successfully",
            class_id=result.class_id,
            data=None
        )

    elif request.operation == 5:  # 删除类别
        class_id = request.class_id_change
        result = annotation_service.delete_class(class_id)
        if result:
            return PromptResponse(
                status="success",
                message=f"Class '{result.class_name}' deleted successfully",
                data=None
            )

        return PromptResponse(
            status="error",
            message="None",
            data=None
        )
    else:
        return PromptResponse(
            status="error",
            message="Invalid operation",
            data=None
        )
