import cv2
from sam_model import SamEncoder, SamDecoder

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
