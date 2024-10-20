from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
from sam_model import SamEncoder, SamDecoder

# encoder = SamEncoder(
#     model_path="models/sam-med2d_b.encoder.onnx",
#     warmup_epoch=3,
#     device="cpu"
# )
# decoder = SamDecoder(
#     model_path="models/sam-med2d_b.decoder.onnx",
#     device="cpu",
# )
# if __name__ == '__main__':
#     encoder_path = "models/sam-med2d_b.encoder.onnx"
#     decoder_path = "models/sam-med2d_b.decoder.onnx"
#
#     # Initialize the SAM-Med2D onnx model
#     encoder = SamEncoder(
#         model_path=encoder_path,
#         warmup_epoch=3,
#         device="cpu"
#     )
#     decoder = SamDecoder(
#         model_path=decoder_path,
#         device="cpu",
#     )
#
#     image_path = "images/amos_0004_75.png"
#     '''Specifying a specific object with a point'''
#     img_file = cv2.imread(image_path)
#     img_embeddings = encoder(img_file)
#
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8132)