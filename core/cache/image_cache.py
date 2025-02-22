# image_cache.py

# 添加一个字典来存储每张图对应的img_embeddings
# 后期可以做个导出工作从本地文件中读取
# 或者用redis存储，故模块化
# key -> value
image_id_cache = {} # image_path -> image_id
# (唯一)class_id
# (唯一)mask_id = str(mask_data.class_id) + "_" +str(len(image_data_cache[image_id].masks[mask_data.class_id]))
image_data_cache = {} # image_id -> image_data (classes, masks, width, height)
# image_data_cache = {
#     1: {
#         "classes": {  
#                     0: "_background_",
#                     1: "class1",
#                     2: "class2"
#                 }, 
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
image_class_cache = {} # class_id -> class_name
# image_class_cache = {
#     0: "_background_",
#     1: "class1",
#     2: "class2"
# }
image_embeddings_cache = {} # image_id -> img_embeddings
current_image_id = 0
def get_current_id():
    global current_id
    return current_id

def set_current_id(new_id):
    global current_id
    current_id = new_id
# 用于字典的反向查找
def find_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None