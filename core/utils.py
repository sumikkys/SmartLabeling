import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

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

