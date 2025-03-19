from initialize_model import clip_text_encoder, clip_vision_encoder
import cv2
import numpy as np
from utils import normalize, softmax, top_k

classes = ["kidney", "liver", "lung"]
image = cv2.imread("/Users/sumipeng/Programming/AI/SmartLabeling/core/images/amos_0507_31.png")

prompt = {
    'points': np.array([[[200,300]]]).astype(np.float32),# (1,1,2) 即 (batch_size, num_points, 2)
    'labels': np.ones((1,1),dtype=np.int32), # (1,1) 即 (batch_size, num_points) 现在只有标签为1的点
}

image_features = clip_vision_encoder(np.array(image), prompt)

# 计算文本特征
classes_features = clip_text_encoder.zeroshot_classifier(classes)

# 对图像和特征进行归一化
image_features_normalized = normalize(image_features)
# 计算相似度
similarity = 100.0 * np.matmul(image_features_normalized, classes_features)
similarity_softmax = softmax(similarity, axis=1)
values, indices = top_k(similarity_softmax, 3)
print("\n相似度结果:")
for i, (val, idx) in enumerate(zip(values[0], indices[0])):
    print(f"排名 {i+1}: {classes[idx]} (相似度: {val:.4f})")