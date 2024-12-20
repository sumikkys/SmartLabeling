import cv2
from sam_model import SamEncoder, SamDecoder


encoder = None
decoder = None

def initialize_models():
    global encoder, decoder

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
