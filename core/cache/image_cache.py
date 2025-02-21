# image_cache.py

# 添加一个字典来存储每张图对应的img_embeddings
# 后期可以做个导出工作从本地文件中读取
# 或者用redis存储，故模块化
image_id_cache = {} # image_path -> image_id
image_data_cache = {} # image_id -> image_data (classes, masks, width, height)
image_embeddings_cache = {} # image_id -> img_embeddings
current_image_id = 0
# 用于字典的反向查找
def find_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None