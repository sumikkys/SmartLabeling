# clip_service.py
import cv2
import numpy as np
from utils import normalize, softmax, top_k
from initialize_model import clip_text_encoder, clip_vision_encoder
from cache.image_cache import *

def clip_class(operation, current_state, image_id: int):
    """使用CLIP识别class"""
    if operation in ['add', 'undo', 'redo']: 
        classes = []
        for class_id, class_name in image_class_cache.items():
            classes.append(class_name)
        if classes == []:
            return None
        # prefix = "a photo of a "
        # texts = [prefix + class_name for class_name in classes]
        image_id = get_current_id()
        image_path = find_key_by_value(image_id_cache, image_id)
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
        else:
            raise ValueError("Boxes is not None")

        image_features = clip_vision_encoder(np.array(image), prompt)

        classes_features = clip_text_encoder.zeroshot_classifier(classes)

        # 对图像和文本特征进行归一化
        image_features_normalized = normalize(image_features)
        # 计算相似度
        similarity = 100.0 * np.matmul(image_features_normalized, classes_features)
        similarity_softmax = softmax(similarity, axis=1)
        values, indices = top_k(similarity_softmax, 3)
        result = {}
        for i, (val, idx) in enumerate(zip(values[0], indices[0])):
            print(f"排名 {i+1}: {classes[idx]} (相似度: {val:.4f})")
            rank_key = f"rank_{i+1}" 
            result[rank_key] = {
                "class": classes[idx],
                "class_id": find_key_by_value(image_class_cache, classes[idx]),
                "probability": float(val)
            }

    return result