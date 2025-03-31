# annotation_tools_service.py
from cache.image_cache import cache_manager
from schemas.annotation_tools_schema import *
from utils import normalize, softmax, top_k

# 在文件开头添加全局计数器
class GlobalCounter:
    def __init__(self):
        self.class_counter = "1"  # 初始化为字符串 "1"
        self.mask_counter = {}    # 每个 image_id 的每个 class_id 对应一个 mask 计数器

    def get_next_class_id(self) -> str:
        """生成下一个 class_id,返回字符串类型"""
        next_id = self.class_counter
        self.class_counter = str(int(self.class_counter) + 1)  # 转换为整数递增后转回字符串
        return next_id

    def get_next_mask_id(self, image_id: str, class_id: str) -> str:
        """生成下一个 mask_id,返回字符串类型"""
        if image_id not in self.mask_counter:
            self.mask_counter[image_id] = {}
        if class_id not in self.mask_counter[image_id]:
            self.mask_counter[image_id][class_id] = 0

        next_id = self.mask_counter[image_id][class_id]
        self.mask_counter[image_id][class_id] += 1
        return f"{class_id}_{next_id}"
    
global_counter = GlobalCounter()

class AnnotationService:

    def add_mask(self,image_id: str, mask_data: MaskData) -> MaskResponse:
        """添加一个新的标注 Mask"""
        if image_id not in cache_manager.image_data_cache:
            return False
        mask_id = global_counter.get_next_mask_id(image_id, mask_data.class_id)
        if cache_manager.image_data_cache[image_id]["masks"].get(mask_data.class_id) is None:
            cache_manager.image_data_cache[image_id]["masks"][mask_data.class_id] = {}  
        cache_manager.image_data_cache[image_id]["masks"][mask_data.class_id][mask_id] = mask_data.masks
        return MaskResponse(mask_id=mask_id, class_id=mask_data.class_id)

    def delete_mask(self, image_id: str, mask_id: str) -> Optional[MaskResponse]:
        """删除标注的 Mask"""
        if image_id not in cache_manager.image_data_cache:
            return MaskResponse(mask_id=mask_id, class_id=None, message="Image ID not found.")
        
        class_id = mask_id.split("_")[0] 
        
        if class_id not in cache_manager.image_data_cache[image_id]["masks"]:
            return MaskResponse(mask_id=mask_id, class_id=class_id, message="Class ID not found in image.")
        
        if mask_id in cache_manager.image_data_cache[image_id]["masks"][class_id]:
            del cache_manager.image_data_cache[image_id]["masks"][class_id][mask_id]
            return MaskResponse(mask_id=mask_id, class_id=class_id, message="Mask deleted successfully.")
        else:
            return MaskResponse(mask_id=mask_id, class_id=class_id, message="Mask ID not found.")

    def update_class_name(self, class_id: str, class_name: str) -> Optional[ClassResponse]:
        """更新类别"""
        if class_id in cache_manager.image_class_cache.keys():
            cache_manager.image_class_cache[class_id] = class_name
            return ClassResponse(class_id=class_id, class_name=class_name)
        return None

    def get_classes(self) -> List[ClassResponse]:
        """获取当前图片所有类别"""
        classes = []
        for class_id, class_name in cache_manager.image_class_cache.items():
            classes.append(ClassResponse(class_id=class_id, class_name=class_name))
        return classes

    def add_class(self, class_name: str) -> Optional[ClassResponse]:
        """添加新类别"""
        if class_name in cache_manager.image_class_cache.values():
            class_id = cache_manager.find_key_by_value(cache_manager.image_class_cache, class_name)
            return ClassResponse(class_id=class_id, class_name=class_name, message="Class already exists.")
        
        class_id = global_counter.get_next_class_id()
        cache_manager.image_class_cache[class_id] = class_name
        return ClassResponse(class_id=class_id, class_name=class_name, message="Class added successfully.")

    def delete_class(self, class_id:str) -> Optional[ClassResponse]:
        """删除类别"""
        if class_id in cache_manager.image_class_cache.keys():
            class_name = cache_manager.image_class_cache[class_id]
            del cache_manager.image_class_cache[class_id]
            return ClassResponse(class_id=class_id, class_name=class_name, message="Class deleted successfully.")
        else:
            return ClassResponse(class_id=class_id, class_name="None", message="Class not found.")

annotation_service = AnnotationService()

def process_prompt(request: PromptRequest) -> PromptResponse:
    """处理来自前端的标注请求"""
    
    image_id = cache_manager.get_current_id()
    
    if image_id not in cache_manager.image_data_cache:
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
