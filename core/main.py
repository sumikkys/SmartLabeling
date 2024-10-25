from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
from sam_model import SamEncoder, SamDecoder
from routers import prompt, upload_image, get_result

# 全局变量
encoder = None
decoder = None
img_embeddings = None
img_file = None

def initialize_models():
    global encoder, decoder, img_embeddings, img_file

    encoder_path = "models/sam-med2d_b.encoder.onnx"
    decoder_path = "models/sam-med2d_b.decoder.onnx"

    # Initialize the SAM-Med2D ONNX model
    encoder = SamEncoder(
        model_path=encoder_path,
        warmup_epoch=3,
        device="cpu"
    )
    decoder = SamDecoder(
        model_path=decoder_path,
        device="cpu",
    )

    image_path = "images/amos_0004_75.png"
    img_file = cv2.imread(image_path)
    img_embeddings = encoder(img_file)

    return img_file, img_embeddings

initialize_models()

app = FastAPI()

app.include_router(prompt.router)
app.include_router(upload_image.router)
app.include_router(get_result.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8232)

# if __name__ == '__main__':
#     encoder_path = "models/sam-med2d_b.encoder.onnx"
#     decoder_path = "models/sam-med2d_b.decoder.onnx"

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

#     image_path = "images/amos_0004_75.png"
#     '''Specifying a specific object with a point'''
#     img_file = cv2.imread(image_path)
#     img_embeddings = encoder(img_file)

#     # 一�?�?
#     # _, logits = decoder.point(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[1])

#     # 两个�? 同时输入上一次的low-resolution mask
#     # decoder.point(img_embeddings, img_file, point_coords=[[324, 282],[314, 177]], point_labels=[1,0], logits=logits)

#     # 边界�?
#     decoder.bBox(img_embeddings, img_file, boxes=[225, 153, 308, 240])

#     # 边界框与点混�?
#     # decoder.hybrid(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[0], boxes=[225, 153, 308, 240])
