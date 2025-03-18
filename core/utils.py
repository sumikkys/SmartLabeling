import matplotlib.pyplot as plt
import numpy as np


def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)


def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels == 1]
    neg_points = coords[labels == 0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white',
               linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white',
               linewidth=1.25)


def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0, 0, 0, 0), lw=2))
    
    
def normalize(v):
    # 计算每行的 L2 范数
    norm = np.sqrt(np.sum(v * v, axis=1, keepdims=True))
    # 避免除以零
    norm = np.where(norm == 0, 1e-10, norm)
    # 归一化
    return v / norm


def softmax(x, axis=None):
    """Compute softmax values for each sets of scores in x."""
    exp_x = np.exp(x - np.max(x, axis=axis, keepdims=True))  # 减去最大值以提高数值稳定性
    return exp_x / np.sum(exp_x, axis=axis, keepdims=True)


def top_k(array, k):
    """返回数组中最大的 k 个值及其索引"""
    if k > array.shape[1]:
        k = array.shape[1]  # 确保 k 不大于数组长度
    
    indices = np.argsort(array, axis=1)[:, -k:][:, ::-1]  # 降序排列索引
    values = np.take_along_axis(array, indices, axis=1)  # 根据索引获取值
    
    return values, indices


med_templates = [
    # 基础描述
    "The highlighted area in this image indicates {text}.",
    "The marked region in this image points to {text}.",
    "This image identifies the area with {text}.",
    "Here, the image captures the existence of {text}.",
    # 针对特定模式的描述
    "The point prompt indicates the {text} in this {modality} image.",
    "Attention is directed to the {text} in this {modality} image.",
    "The point prompt points to the {text} in this {modality} image.",
    "The {text} area is the main focus of this medical imagery.",
    "The highlighted area in this {modality} scan pertains to the {text}.",
    "Consider the {text} area as the region of interest in this {modality} scan.",
    # 深入描述
    "The {text} region is the point of interest in this {modality} scan.",
    "Focus on the specified {text} area within this {modality} image.",
    "The {text} is highlighted as the key area in this {modality} scan.",
    "Concentrate on the {text} region in this {modality} image.",
    "The {text} is the indicated region in this {modality} scan.",
    "The key focus in this {modality} image is the {text} area.",
    # 详细说明
    "This {modality} scan directs attention to the {text}.",
    "Highlighting the {text} region in this {modality} image.",
    "This {modality} image focuses on the {text} region.",
    "The area of interest in this {modality} scan is the {text}.",
    "This {modality} scan centers on the {text} area.",
    "The {text} section is the focus of this {modality} image.",
    # 针对特定区域的描述
    "The primary area of interest in this {modality} image is the {text}.",
    "The target area in this {modality} image is the {text}.",
    "The {text} is the specified region in this {modality} scan.",
    "Attention is directed to the {text} area in this {modality} scan.",
    "This {modality} image centers on the {text}.",
    "The {text} region is marked in this {modality} scan.",
    # 特定区域的详细描述
    "Look at the {text} section in this {modality} image.",
    "The highlighted part of this {modality} scan is the {text}.",
    "This {modality} scan is focused on the {text}.",
    "The {text} is the area of focus in this {modality} image.",
    "This {modality} image emphasizes the {text} region.",
    "The {text} is the indicated area in this {modality} scan.",
    # 重点区域描述
    "The target region in this {modality} scan is the {text}.",
    "Pay attention to the {text} in this {modality} image.",
    "The {text} is highlighted in this {modality} scan.",
    "In this {modality} image, the {text} is the point of interest.",
    "This {modality} scan points to the {text} area.",
    "The {text} area is the focus in this {modality} image.",
    # 进一步详细描述
    "This {modality} image shows the {text} region as the area of interest.",
    "The {text} is the key region in this {modality} scan.",
    "Focus your attention on the {text} in this {modality} scan.",
    "The primary area in this {modality} image is the {text}.",
    "The {text} is the highlighted region in this {modality} scan.",
    
    "This {modality} image reveals the {text} area.",
    "The {text} can be seen in this {modality} scan.",
    "Highlighted here is the {text} in this {modality} image.",
    "The {text} region stands out in this {modality} scan.",
    "The {text} is prominently shown in this {modality} image.",
    "This {modality} scan highlights the {text} area of interest.",
    "The {text} part is evident in this {modality} image.",
    "This image from {modality} demonstrates the {text}.",
    "The {text} is clearly visible in this {modality} scan.",
    "The {text} section is emphasized in this {modality} image.",
    "In this {modality} scan, the {text} is the focus region.",
    "This {modality} image directs focus to the {text}.",
    "The {text} area is discernible in this {modality} scan.",
    "Highlighted in this {modality} image is the {text}.",
    "The {text} region is apparent in this {modality} scan.",
    "This {modality} scan shows {text}."
    
]