from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
from sam_model import SamEncoder, SamDecoder
from initialize_model import initialize_models

#     # 一个点
#     # _, logits = decoder.point(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[1])
#
#     # 两个点 同时输入上一次的low-resolution mask
#     # decoder.point(img_embeddings, img_file, point_coords=[[324, 282],[314, 177]], point_labels=[1,0], logits=logits)
#
#     # 边界框
#     decoder.bBox(img_embeddings, img_file, boxes=[225, 153, 308, 240])
#
#     # 边界框与点混合
#     # decoder.hybrid(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[0], boxes=[225, 153, 308, 240])

app = FastAPI()

initialize_models()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8132)