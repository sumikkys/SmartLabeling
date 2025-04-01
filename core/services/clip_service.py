# clip_service.py
import cv2
import numpy as np
from utils import normalize, softmax, top_k
from initialize_model import clip_vision_encoder
from cache.image_cache import cache_manager

def clip_class(operation, current_state, image_id: str, classes_features: np.ndarray):
    """使用CLIP识别class"""
    if operation in ['add', 'undo', 'redo']: 

        classes = []
        for class_id, class_name in cache_manager.image_class_cache.items():
            classes.append(class_name)
        if classes == []:
            return None
        if classes_features.any() == False:
            return None

        # prefix = "a photo of a "
        # texts = [prefix + class_name for class_name in classes]
        image_id = cache_manager.get_current_id()
        image_path = cache_manager.find_key_by_value(cache_manager.image_id_cache, image_id)
        image = cv2.imread(image_path)
        #001 011
        if (not current_state['foreground'] and current_state['boxes']):
            box1 = current_state["boxes"][-1][0:2] #左上
            box2 = current_state["boxes"][-1][2:4] #右下
            prompt = {
                'points': np.array([[box1,box2]]).astype(np.float32),
                'labels': np.array([[2, 3]], dtype=np.int32),  
            }
        #101 111
        elif (current_state['boxes']):
            box1 = current_state["boxes"][-1][0:2]
            box2 = current_state["boxes"][-1][2:4]
            point = current_state['foreground'][-1]
            prompt = {
                'points': np.array([[box1,box2,point]]).astype(np.float32),
                'labels': np.array([[2, 3, 1]], dtype=np.int32), 
            }
        #100 110
        elif (current_state['foreground']):
            point = current_state['foreground'][-1]
            prompt = {
                'points': np.array([[point]]).astype(np.float32),
                'labels': np.ones((1,1), dtype=np.int32),  
            }
        #010 000
        else:
            raise ValueError("The available data is not None")

        image_features = clip_vision_encoder(np.array(image), prompt)

        # classes_features = clip_text_encoder.zeroshot_classifier(classes)
        classes_features = classes_features

        # 对图像和文本特征进行归一化
        image_features_normalized = normalize(image_features)
        # 计算相似度
        similarity = 100.0 * np.matmul(image_features_normalized, classes_features)
        similarity_softmax = softmax(similarity, axis=1)
        values, indices = top_k(similarity_softmax, 3)
        result = {}
        for i, (val, idx) in enumerate(zip(values[0], indices[0])):
            if idx < len(classes):
                print(f"排名 {i+1}: {classes[idx]} (相似度: {val:.4f})")
                rank_key = f"rank_{i+1}" 
                result[rank_key] = {
                    "class": classes[idx],
                    "class_id": cache_manager.find_key_by_value(cache_manager.image_class_cache, classes[idx]),
                    "probability": float(val)
                }

    return result